# Allow attribute and variable names in the first column of the attribute and
# variable tables to wrap after an underscore, by inserting <wbr> there.
WBR_TABLE = %r{<table class="(?:attribute|variable)-table">.*?</table>}m
WBR_NAME = %r{(<tr>\s*<td><code[^>]*>)([^<]*)(</code>)}

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html"

  doc.output = doc.output.gsub(WBR_TABLE) do |table|
    table.gsub(WBR_NAME) { "#{$1}#{$2.gsub('_', '_<wbr>')}#{$3}" }
  end
end
