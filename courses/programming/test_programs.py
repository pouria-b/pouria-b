"""Build and run regression tests. Requires Python 3.9+ and g++ with C++17."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent


class Programs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.bins={}
        for name in ('hill_cipher','sudoku'):
            exe=Path(cls.temp.name)/name
            subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Wpedantic','-Werror',str(ROOT/(name+'.cpp')),'-o',str(exe)],check=True)
            cls.bins[name]=str(exe)

    def run_program(self,name,*args,input=''):
        return subprocess.run([self.bins[name],*args],input=input,text=True,capture_output=True,timeout=10)

    def test_hill_known_vector(self):
        r=self.run_program('hill_cipher','GYBNQKURP','ACT')
        self.assertEqual(r.returncode,0);self.assertEqual(r.stdout.strip(),'POH')

    def test_hill_normalization_and_blocks(self):
        r=self.run_program('hill_cipher','gybnqkurp','actact')
        self.assertEqual(r.stdout.strip(),'POHPOH')
        self.assertEqual(self.run_program('hill_cipher','BAAABAAAB','ABCXYZ').stdout.strip(),'ABCXYZ')

    def test_hill_rejects_invalid_input(self):
        for key,message in [('SHORT','ACT'),('AAAAAAAAA','ACT'),('GYBNQKURP','A'),('GYBNQKURP',''),('GYBNQKURP','A C'),('GYBNQKURP','123'),('GYBNQKUR!','ACT')]:
            self.assertEqual(self.run_program('hill_cipher',key,message).returncode,1)

    def test_hill_interactive_multiple_messages_and_eof(self):
        r=self.run_program('hill_cipher',input='GYBNQKURP\nACT\nACT\n!!!\n')
        self.assertEqual(r.returncode,0);self.assertEqual(r.stdout.count('POH'),2)
        self.assertEqual(self.run_program('hill_cipher',input='GYBNQKURP\n').returncode,0)

    def assert_solution(self,result,clues):
        self.assertEqual(result.returncode,0,result.stderr)
        values=list(map(int,result.stdout.split()));self.assertEqual(len(values),81)
        board=[values[i:i+9] for i in range(0,81,9)];digits=set(range(1,10))
        for row in board:self.assertEqual(set(row),digits)
        for c in range(9):self.assertEqual({board[r][c] for r in range(9)},digits)
        for rr in (0,3,6):
            for cc in (0,3,6):self.assertEqual({board[r][c] for r in range(rr,rr+3) for c in range(cc,cc+3)},digits)
        for i,value in enumerate(clues):
            if value:self.assertEqual(values[i],value)
        return values

    def test_sudoku_example_file_and_stdin(self):
        path=ROOT/'examples/sudoku.dat';text=path.read_text();clues=list(map(int,text.split()))
        a=self.run_program('sudoku',str(path));self.assert_solution(a,clues)
        self.assertEqual(a.stdout,self.run_program('sudoku',input=text).stdout)

    def test_sudoku_solved_board(self):
        text=(ROOT/'examples/sudoku.dat').read_text()
        solution=self.run_program('sudoku',input=text).stdout
        self.assertEqual(self.run_program('sudoku',input=solution).stdout,solution)

    def test_sudoku_empty_board(self):
        self.assert_solution(self.run_program('sudoku',input='0 '*81),[0]*81)

    def test_sudoku_invalid_file_and_cells(self):
        self.assertEqual(self.run_program('sudoku','/nonexistent/sudoku.dat').returncode,1)
        for text in ('0 '*80,'0 '*82,'10 '+'0 '*80,'-1 '+'0 '*80,'x '+'0 '*80,'1 1 '+'0 '*79):
            self.assertEqual(self.run_program('sudoku',input=text).returncode,1)

    def test_sudoku_unsatisfiable(self):
        clues=(ROOT/'examples/sudoku.dat').read_text().split();clues[2]='1'
        r=self.run_program('sudoku',input=' '.join(clues))
        self.assertEqual(r.returncode,2,r.stderr)
        self.assertEqual(r.stdout,'');self.assertIn('No solution',r.stderr)


if __name__=='__main__':unittest.main()
