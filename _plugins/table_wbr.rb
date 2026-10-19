# Allow attribute and variable names in the first column of the attribute and
# variable tables to wrap after an underscore, by inserting <wbr> there.
WBR_TABLE = %r{<table class="(?:[^"]*\s)?(?:attribute|variable|mandatory-attribute)-table(?:\s[^"]*)?">.*?</table>}m
WBR_NAME = %r{(<tr>\s*<td><code[^>]*>)([^<]*)(</code>)}

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html"

  doc.output = doc.output.gsub(WBR_TABLE) do |table|
    # Take the groups before the inner gsub, which resets $1, $2 and $3.
    table.gsub(WBR_NAME) do
      open, name, close = $1, $2, $3
      "#{open}#{name.gsub('_', '_<wbr>')}#{close}"
    end
  end
end
