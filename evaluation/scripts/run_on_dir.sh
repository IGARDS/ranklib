GRAPH_DIR=$1
SCRIPT="find_k_wrapper.py"
for graph_path in `ls $GRAPH_DIR/*.csv | egrep -v _50 | egrep -v _100 | egrep -v fully`; do
  echo ./generic_wrapper.sh ./$SCRIPT $graph_path
  ./generic_wrapper.sh ./$SCRIPT $graph_path >$graph_path.$SCRIPT.json 2>$graph_path.$SCRIPT.err
done;
