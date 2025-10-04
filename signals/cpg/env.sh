for i in $(env | grep MY_)
do 
    key=$(echo $i | cut -d '=' -f 1)
    value=$(echo $i | cut -d '=' -f 2-)
    echo $key=$value 
    # sed ALL files. 
    # find /usr/share/nginx/html -type -f -exec sed -i "s|${key}|${value}|g" '{}' +
    
    # sed JS and CSS only 
    find /usr/share/nginx/html -type f \( -name '*.js' -o -name '*.css' \) -exec sed
done