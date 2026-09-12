import unittest
import numpy as np
import pandas as pd
from compass import Config, signals, backtest, ASSETS

class EngineTests(unittest.TestCase):
    def data(self):
        dates=pd.bdate_range('2020-01-01',periods=400)
        columns=['SPY','XLE','XLK','XLU','XLP','IEF','XLI','XLF','XLB','XLV']
        p=pd.DataFrame({c:100*np.exp(np.arange(400)*(.001+i*.0001)) for i,c in enumerate(columns)},index=dates)
        f=pd.Series(2.2+np.arange(400)*.001,index=dates)
        return p,f

    def test_future_does_not_change_past_signals(self):
        p,f=self.data(); old=signals(p,f)
        p.iloc[300:]*=4; f.iloc[300:]=1
        new=signals(p,f)
        pd.testing.assert_frame_equal(old.iloc[:300],new.iloc[:300])

    def test_lag_delays_fred(self):
        p,f=self.data(); s=signals(p,f,Config(fred_lag=1))
        self.assertEqual(s.breakeven.iloc[250],f.iloc[249])

    def test_exact_indicator_formula(self):
        p,f=self.data(); s=signals(p,f)
        r=p.pct_change(fill_method=None)
        positive=.5*r.XLE+(r.XLI+r.XLF+r.XLB)/6
        negative=(r.XLU+r.XLV+r.XLP)/3
        expected=(1+positive.fillna(0)).cumprod()/(1+negative.fillna(0)).cumprod()
        np.testing.assert_allclose(s.positive_basket_return.iloc[1:],positive.iloc[1:])
        np.testing.assert_allclose(s.negative_basket_return.iloc[1:],negative.iloc[1:])
        np.testing.assert_allclose(s.inflation_indicator,expected)

    def test_exact_four_conditions_and_or_rule(self):
        p,f=self.data(); s=signals(p,f)
        valid=s.valid
        self.assertTrue((s.loc[valid,'growth_up']==(s.loc[valid,'spy']>s.loc[valid,'sma'])).all())
        self.assertTrue((s.loc[valid,'level_above_target']==(s.loc[valid,'breakeven']>2.0)).all())
        self.assertTrue((s.loc[valid,'breakeven_momentum_positive']==(s.loc[valid,'breakeven_change']>0)).all())
        self.assertTrue((s.loc[valid,'asset_momentum_positive']==(s.loc[valid,'basket_slope']>0)).all())
        combined=s.level_above_target & (s.breakeven_momentum_positive | s.asset_momentum_positive)
        self.assertTrue((s.loc[valid,'inflation_on']==combined.loc[valid]).all())

    def test_mixed_holdings_drift_and_execution_delay(self):
        p,f=self.data(); s=signals(p,f)
        s['regime']='slowdown'; s['valid']=True
        cfg=Config(execution_lag=1)
        nav,_,events,_=backtest(p,s,'2020-01-01','2020-03-15',cfg)
        self.assertEqual(events.iloc[0].signal_date,pd.Timestamp('2020-01-31'))
        self.assertEqual(nav.index[0],pd.Timestamp('2020-02-03'))
        before=nav.loc[:'2020-02-28']
        expected=.5*p.loc[before.index,'XLP']/p.loc[before.index[0],'XLP']+.5*p.loc[before.index,'IEF']/p.loc[before.index[0],'IEF']
        np.testing.assert_allclose(before,expected)

    def test_initial_cost_and_no_same_day_return(self):
        p,f=self.data(); s=signals(p,f); s['valid']=True; s['regime']='reflation'
        cfg=Config(cost_bps=10)
        nav,_,events,_=backtest(p,s,'2020-01-01','2020-03-01',cfg)
        self.assertAlmostEqual(nav.iloc[0],.999)
        self.assertAlmostEqual(events.iloc[0].turnover,1)

if __name__=='__main__': unittest.main()
