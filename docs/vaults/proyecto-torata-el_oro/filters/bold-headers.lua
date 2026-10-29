-- Filtro de Pandoc para poner en negrita automáticamente todas las celdas de la cabecera (primera fila) de cualquier tabla.
function Table(el)
  if el.thead and el.thead.rows then
    for _, row in ipairs(el.thead.rows) do
      for _, cell in ipairs(row.cells) do
        cell.contents = { pandoc.Strong(cell.contents) }
      end
    end
  end
  return el
end

