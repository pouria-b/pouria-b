import random
import unittest
from scheduling import simulate, round_robin_scheduling, srtf_scheduling


class SchedulingTests(unittest.TestCase):
    def test_fcfs_unsorted(self):
        r = simulate(['late','early'], [5,0], [2,3], context_switch=1)
        self.assertEqual(r.completion_time, (7,3))
        self.assertEqual(r.gantt_chart, ((0,3,'early'),(3,5,'IDLE'),(5,7,'late')))

    def test_rr_arrival_before_requeue(self):
        r = round_robin_scheduling(['A','B'], [4,1], [0,1], 2, 0)
        self.assertEqual(r.gantt_chart, ((0,2,'A'),(2,3,'B'),(3,5,'A')))
        self.assertEqual(r.completion_time, (5,3))

    def test_no_switch_for_same_process_or_after_finish(self):
        for policy in ('fcfs','rr','spn','srtf','hrrn','mlfq'):
            r = simulate(['A'], [0], [12], policy, quantum=2, context_switch=3)
            self.assertEqual(r.gantt_chart, ((0,12,'A'),))
            self.assertEqual(r.waiting_time, (0,))

    def test_real_switch_cost(self):
        r = simulate(['A','B'], [0,0], [1,1], context_switch=2)
        self.assertEqual(r.gantt_chart, ((0,1,'A'),(1,3,'CS'),(3,4,'B')))
        self.assertEqual(r.waiting_time, (0,3))

    def test_srtf_immediate_preemption(self):
        r = srtf_scheduling(['A','B'], [0,1], [8,1], quantum=5)
        self.assertEqual(r.gantt_chart, ((0,1,'A'),(1,2,'B'),(2,9,'A')))
        self.assertEqual(r.completion_time, (9,2))

    def test_arrival_during_switch(self):
        r = simulate(['A','B','C'], [0,1,2], [8,3,1], 'srtf', context_switch=2)
        self.assertEqual(r.gantt_chart[:3], ((0,1,'A'),(1,3,'CS'),(3,4,'C')))

    def test_spn_nonpreemptive_and_arrival_ties(self):
        r = simulate(['A','B','C'], [0,1,1], [5,3,1], 'spn')
        self.assertEqual(r.completion_time, (5,9,6))
        self.assertEqual(simulate(['A','B'],[0,0],[1,1],'spn').completion_time,(1,2))

    def test_hrrn_uses_waiting_ratio(self):
        r = simulate(['A','B','C'], [0,1,7], [8,4,1], 'hrrn')
        self.assertEqual(r.completion_time, (8,12,13))

    def test_mlfq_demotes_and_reaches_bottom(self):
        r = simulate(['A','B'], [0,0], [10,10], 'mlfq', quantum=2)
        self.assertEqual(r.gantt_chart, ((0,2,'A'),(2,4,'B'),(4,8,'A'),
                                        (8,12,'B'),(12,16,'A'),(16,20,'B')))

    def test_mlfq_preemption_retains_budget(self):
        r = simulate(['A','B','C'], [0,3,8], [10,1,1], 'mlfq', quantum=2)
        self.assertEqual(r.gantt_chart, ((0,3,'A'),(3,4,'B'),(4,8,'A'),
                                        (8,9,'C'),(9,12,'A')))

    def test_validation_and_empty(self):
        self.assertEqual(simulate([],[],[]).gantt_chart, ())
        for kwargs in ({'quantum':0},{'context_switch':-1},{'quantum':True}):
            with self.assertRaises(ValueError): simulate(['A'],[0],[1],**kwargs)
        for names, arrivals, bursts in ((['A'],[],[1]),(['A'],[-1],[1]),
                                        (['A'],[0],[0]),(['CS'],[0],[1]),
                                        (['A','A'],[0,0],[1,2]),(['A'],[0.5],[1])):
            with self.assertRaises(ValueError): simulate(names,arrivals,bursts)

    def test_random_workload_invariants(self):
        rng = random.Random(2026)
        for policy in ('fcfs','rr','spn','srtf','hrrn','mlfq'):
            for _ in range(40):
                names = ['P'+str(i) for i in range(rng.randint(1,6))]
                arrivals = [rng.randrange(10) for _ in names]
                bursts = [rng.randint(1,9) for _ in names]
                saved = (names[:],arrivals[:],bursts[:])
                r = simulate(names,arrivals,bursts,policy,quantum=2,context_switch=1)
                self.assertEqual((names,arrivals,bursts),saved)
                executed = dict.fromkeys(names,0)
                first, last = {}, {}
                previous_end = 0
                for start,end,label in r.gantt_chart:
                    self.assertEqual(start,previous_end)
                    self.assertGreater(end,start)
                    previous_end = end
                    if label in executed:
                        i=names.index(label)
                        self.assertGreaterEqual(start,arrivals[i])
                        executed[label]+=end-start
                        first.setdefault(label,start)
                        last[label]=end
                self.assertEqual(r.gantt_chart[-1][2] in ('CS','IDLE'),False)
                for i,name in enumerate(names):
                    self.assertEqual(executed[name],bursts[i])
                    self.assertEqual(last[name],r.completion_time[i])
                    self.assertEqual(first[name]-arrivals[i],r.response_time[i])
                    self.assertEqual(r.waiting_time[i],r.completion_time[i]-arrivals[i]-bursts[i])
                    self.assertGreaterEqual(r.waiting_time[i],0)

    def test_srtf_against_independent_zero_overhead_oracle(self):
        rng = random.Random(71)
        for _ in range(80):
            arrivals=[rng.randrange(8) for _ in range(4)]
            bursts=[rng.randint(1,7) for _ in range(4)]
            rem=bursts[:]; completed=[0]*4; t=0; previous=None
            while any(rem):
                available=[i for i in range(4) if arrivals[i]<=t and rem[i]]
                if not available:
                    t+=1;previous=None;continue
                minimum=min(rem[i] for i in available)
                i=previous if previous in available and rem[previous]==minimum else min(available,key=lambda j:(rem[j],arrivals[j],j))
                rem[i]-=1;t+=1;previous=i
                if rem[i]==0:completed[i]=t
            self.assertEqual(simulate(['A','B','C','D'],arrivals,bursts,'srtf').completion_time,tuple(completed))


if __name__ == '__main__':
    unittest.main()
