. common_script.sh
cat common_script.sh > vpl_execution
echo "nadia -i $VPL_SUBFILE0 -t \" A,B |- A&B\" " >> vpl_execution
chmod +x vpl_execution