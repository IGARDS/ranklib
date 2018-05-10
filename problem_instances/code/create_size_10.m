ntimes = 10;
n = 10;
rnorm = zeros(1,ntimes);
for j = 1:ntimes
    D=round(rand(n,n));
    for i = 1:size(D,1)
        D(i,i) = 0;
    end
    [k,p,P,stats] = rankability_exhaustive_parallel(D,100,'transform',true);
    extra = {};
    extra.r = stats.r;
    extra.rtransformed = stats.rtransformed;
    save_instance(D,k,P',extra,'empirical',['random_',num2str(n),'_',num2str(j),'.json']);
end