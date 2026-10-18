$src = "d:\07_Ciclo\septimo_ciclo\public_investment_projects\docs\vaults\proyecto-torata-el_oro\levantamiento_de_informacion\ficha_indicadores_territoriales.docx"
$dst = "d:\07_Ciclo\septimo_ciclo\public_investment_projects\docs\vaults\proyecto-torata-el_oro\levantamiento_de_informacion\ficha_indicadores_territoriales.pdf"
$siteDst = "d:\07_Ciclo\septimo_ciclo\public_investment_projects\_site\docs\vaults\proyecto-torata-el_oro\levantamiento_de_informacion\ficha_indicadores_territoriales.pdf"

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($src)
    $doc.SaveAs([ref]$dst, [ref]17)
    $doc.Close()
    $word.Quit()
    Copy-Item $dst $siteDst -Force
    Write-Host "PDF generado exitosamente"
} catch {
    Write-Host "Word COM error: $_"
}
