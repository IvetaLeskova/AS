"""Run each architecture test suite independently and export actual test results."""
from pathlib import Path
import subprocess, sys, csv, re, argparse
ROOT=Path(__file__).resolve().parent
VERSIONS=('layered','modular-monolith','hexagonal')
parser=argparse.ArgumentParser()
parser.add_argument('--baseline',type=Path,help='Saved baseline project-1 directory before an experiment')
parser.add_argument('--label',default='baseline',help='Experiment label')
args=parser.parse_args()
rows=[]
for version in VERSIONS:
    folder=ROOT/version
    cmd=[sys.executable,'-m','pytest','tests','-q','--cov=app','--cov-report=term']
    print('\n====',version,'====',flush=True)
    result=subprocess.run(cmd,cwd=folder,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print(result.stdout)
    passed=re.search(r'(\d+) passed',result.stdout)
    failures=re.search(r'(\d+) failed',result.stdout)
    coverage=re.search(r'^TOTAL\s+\d+\s+\d+\s+(\d+)%',result.stdout,re.M)
    row={'experiment':args.label,'architecture':version,'passed_tests':int(passed.group(1)) if passed else 0,'failed_tests':int(failures.group(1)) if failures else (0 if result.returncode==0 else -1),'coverage_percent':int(coverage.group(1)) if coverage else '', 'test_exit_code':result.returncode,'changed_files':'','added_lines':'','deleted_lines':''}
    if args.baseline:
        old=args.baseline/version/'app';new=folder/'app'
        diff=subprocess.run(['git','diff','--no-index','--numstat','--',str(old),str(new)],capture_output=True,text=True)
        if diff.returncode not in (0,1):raise RuntimeError(diff.stderr)
        files=adds=dels=0
        for line in diff.stdout.splitlines():
            parts=line.split('\t')
            if len(parts)!=3:continue
            files+=1
            if parts[0].isdigit():adds+=int(parts[0])
            if parts[1].isdigit():dels+=int(parts[1])
        row.update(changed_files=files,added_lines=adds,deleted_lines=dels)
    rows.append(row)
output=ROOT/f'results_{args.label}.csv'
with output.open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
print('\nSaved actual results:',output)
if any(r['test_exit_code']!=0 for r in rows):sys.exit(1)
