ntimes = 100;
n = 7;
rnorm = zeros(1,ntimes);
max_value = 20;
min_spread = 5;
for j = 1:ntimes
    D=round(max_value*rand(n,n));
    for i = 1:size(D,1)
        D(i,i) = 0;
    end
    for i = 1:size(D,1)
        for k = (i+1):size(D,1)
            diff = abs(D(i,k) - D(k,i));
            if diff < min_spread
                D(i,k) = 0;
                D(k,i) = 0;
            end
        end
    end
    [k,p,P,stats] = rankability_exhaustive(D,'transform',true);
    extra = {};
    extra.r = stats.r;
    extra.rtransformed = stats.rtransformed;
    save_instance(D,k,P',extra,'empirical',['random_weighted_',num2str(n),'_',num2str(j),'.json']);
end