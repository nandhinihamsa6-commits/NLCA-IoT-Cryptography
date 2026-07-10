import argparse, json
from pathlib import Path
from nlca.benchmarking import benchmark_nlca

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--size",type=int,default=1024*1024)
    p.add_argument("--repetitions",type=int,default=30)
    args=p.parse_args()
    result=benchmark_nlca(args.size,args.repetitions)
    Path("results").mkdir(exist_ok=True)
    Path("results/benchmark.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!="samples_ns"},indent=2))

if __name__=="__main__":
    main()
