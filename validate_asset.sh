#!/bin/bash
# search for unused image assets



search_dir=$1

root_dir=$2

file_name=$3

if [ -z $root_dir ];then
root_dir="$(dirname "$(dirname "$search_dir")")"
fi



echo "search under" "$root_dir"

if [ -z "$file_name" ]; then

for entry in "$search_dir"/*
do
echo "Looking into""$entry"

filename=`basename $entry`

if [ -d $entry ] && [ ${filename: -3} == "set" ]; then

filename="${filename%.*}"
#pattern="named: \"$filename"
#echo "try find" $pattern
#
#pattern1="named:\"$filename"
#echo "try find" $pattern1
file_pattern="\"$filename\""
file_pattern1="=\s$filename"
echo "try find" $file_pattern "under" $root_dir
grep --color --include=\*.{swift,pbxproj,xcworkspace} -rnw $root_dir -e $file_pattern -e $file_pattern1
exist1=$?

storyboad_pattern="name=\"$filename\""
storyboad_pattern1="image=\"$filename\""
grep --color --include=\*.storyboard -rnw $root_dir -e $storyboad_pattern -e $storyboad_pattern1
exist2=$?

if [ "$exist1" -eq 0 ] || [ "$exist2" -eq 0 ];then
echo "pass"
else
echo "remove" $entry
rm -rf $entry
fi

fi

done
else

grep --color --include=\*.{swift,storyboard,pbxproj,xcworkspace} -rnw $root_dir -e $file_name

fi


