.\.venv\Scripts\Activate.ps1

# pip freeze > requirements.txt

$modules = Get-Content -Path requirements.txt
foreach ($module in $modules) {
    # Write-Host $module
    $name = $module.Split("=")[0]
    #   $version = $module.Split("=")[1]
    #   Write-Host "¿Quieres actualizar $name?"
    $respuesta = Read-Host -Prompt "UPDATE pip $name [Write 1 to continue]"
    if ($respuesta -eq 1) {
        Write-Host "Actualizando $name..."
        pip install --upgrade $name
    }
}