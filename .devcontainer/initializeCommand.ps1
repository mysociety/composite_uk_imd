$Folder = 'src/data_common/src'
"Test to see if folder [$Folder] exists"
if (Test-Path -Path $Folder) {
    echo  "Submodule already exists"
} else {
    git submodule update --init
}