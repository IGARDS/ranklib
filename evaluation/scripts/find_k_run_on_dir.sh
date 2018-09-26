GRAPH_DIR=$1
SCRIPT="find_k_wrapper.py"
for graph_path in `ls $GRAPH_DIR/*.csv`; do
  echo ./generic_wrapper.sh ./$SCRIPT $graph_path
  ./generic_wrapper.sh ./$SCRIPT $graph_path >$graph_path.$SCRIPT.json 2>$graph_path.$SCRIPT.err
done;
