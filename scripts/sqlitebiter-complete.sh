_sqlitebiter_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _SQLITEBITER_COMPLETE=complete $1 ) )
    return 0
}

complete -F _sqlitebiter_completion -o default sqlitebiter;
