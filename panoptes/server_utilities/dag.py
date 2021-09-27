from pprint import pprint
from .Graph import Graph


def produce_dag_spec(workflow, jobs):
    #pprint(workflow)
    # TODO build the graphiz script for the DAG based on db data
    example = 'digraph snakemake_dag {\\\n\
    graph[bgcolor=white, margin=0];\\\n\
    node[shape=box, style=rounded, fontname=sans,fontsize=10, penwidth=2];\\\n\
    edge[penwidth=2, color=grey];\\\n\
    0[label = "finish", color = "0.00 0.6 0.85", style="rounded, dashed"];\\\n\
    1[label = "merge_results", color = "0.27 0.6 0.85", style="rounded"];\\\n\
    2[label = "HTSeq_count", color = "0.53 0.6 0.85", style="rounded"];\\\n\
    3[label = "samtools_sort, sample: control_rep1", color = "0.40 0.6 0.85", style="rounded,dashed"];\\\n\
    4[label = "samtools_index", color = "0.13 0.6 0.85", style="rounded"];\\\n\
    5[label = "HTSeq_count", color = "0.53 0.6 0.85", style="rounded"];\\\n\
    6[label = "samtools_sort, sample: control_rep2", color = "0.40 0.6 0.85", style="rounded,dashed"];\\\n\
    7[label = "samtools_index", color = "0.13 0.6 0.85", style="rounded"];\\\n\
    8[label = "HTSeq_count", color = "0.53 0.6 0.85", style="rounded"];\\\n\
    9[label = "samtools_sort, sample: HNRNPCKD_rep1", color = "0.40 0.6 0.85", style="rounded,dashed"];\\\n\
    10[label = "samtools_index", color = "0.13 0.6 0.85", style="rounded"];\\\n\
    11[label = "HTSeq_count", color = "0.53 0.6 0.85", style="rounded"];\\\n\
    12[label = "samtools_sort, sample: HNRNPCKD_rep2", color = "0.40 0.6 0.85", style="rounded,dashed"];\\\n\
    13[label = "samtools_index", color = "0.13 0.6 0.85", style="rounded"];\\\n\
    1 -> 0\\\n\
    2 -> 1\\\n\
    5 -> 1\\\n\
    8 -> 1\\\n\
    11 -> 1\\\n\
    3 -> 2\\\n\
    4 -> 2\\\n\
    3 -> 4\\\n\
    6 -> 5\\\n\
    7 -> 5\\\n\
    6 -> 7\\\n\
    9 -> 8\\\n\
    10 -> 8\\\n\
    9 -> 10\\\n\
    12 -> 11\\\n\
    13 -> 11\\\n\
    12 -> 13\\\n\
}'.encode('utf-8')
    print(example)
    return example


def create_dug_from_db(jobs):
    jobs_list = jobs.all()
    size = len(jobs_list)
    graph = Graph(size)
    for job in jobs_list:
        pprint(job.get_job_json())
        graph.add_node(job.get_job_json())
    return graph.export_agraph()
