from pquisby.lib.post_processing import QuisbyProcessing,BenchmarkName,InputType


a = QuisbyProcessing
b = InputType
c = BenchmarkName

sws=a.extract_data(a,c.FIO,"daaset_1",b.OTHER_FILE,"/Users/soumyasinha/Workspace/2022/rocky_rhel_gvnic/gcp_regression/e2-highcpu-32/fio_run_rt=120/fio_bs_4,1024_iod_1_ndisks_1_disksize_5.86_TiB_njobs_1_2022.12.06T19.00.12/result.csv")
print(sws)


