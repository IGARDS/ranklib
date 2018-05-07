function save_instance(D,k,P,extra,type,file)
if strcmp(type,'empirical') || strcmp(type,'theoretical') || strcmp(type,'partial')
    data = {};
    data.D = D;
    data.k = k;
    if size(P,1) == size(D,1)
       error
    end
    data.P = P;
    data.extra = extra;
    data.type = type;
    text = jsonencode(data);
    fid = fopen(file,'wt');
    fprintf(fid, '%s',text);
    fclose(fid);
else
    disp('Invalid arguments');
end