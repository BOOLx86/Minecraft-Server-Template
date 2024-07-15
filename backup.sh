#!/bin/bash

# Parameters
if [ "$1" == "--verbose" ] || [ "$1" == "-v" ] ; then
    verbose="--verbose"
fi

# Go through every backup entry in config.json
for BACKUP in $(cat ./config.json                           | \
                    sed "s:\$(date):$(date '+%Y-%m-%d'):"   | \
                    sed "s:\$(id):$(date '+%s'):"           | \
                jq -r '."backups"[] | @base64' )
do
    # Backup function, usage: backup [from] [to] [name]
    function backup {
        if [ -f "$1" ] ; then
            echo -e "$(tput bold)Backing up $3...$(tput sgr0)"
            cp "$1" "$2" $verbose | sed 's/^/  /'
        elif [ -d "$1" ] ; then
            echo -e "$(tput bold)Backing up $3...$(tput sgr0)"
            cp "$1" "$2" -r -T $verbose | sed 's/^/  /'
        fi
    }

    # Create any missing directories
    mkdir -p "$( echo "$BACKUP" | base64 --decode | jq -r '."to"' | sed 's:[^\/]*\/*$::' )"

    # Create a backup of given files/folders
    backup  "$( echo "$BACKUP" | base64 --decode | jq -r '."from"' )" \
            "$( echo "$BACKUP" | base64 --decode | jq -r '."to"'   )" \
            "$( echo "$BACKUP" | base64 --decode | jq -r '."name"' )"
done

# Create info file and update "latest save"
if [ ! -f info.json ] ; then
    echo "{\"latest save\" : \"$(date '+%d-%m-%Y__%s')\"}" | jq . > info.json
else
    cat info.json | jq ".\"latest save\" = \"$(date '+%d-%m-%Y__%s')\"" > info.json
fi

if [ "$verbose" == "--verbose" ] ; then
    id=" ($(date '+%s'))"
fi
echo -e "\n$(tput bold)Successfully finished backup!$(tput sgr0)$id\n"
