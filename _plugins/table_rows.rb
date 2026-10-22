# Post-process the attribute and variable tables:
#
# - Give each row an id, so that links can point to the definition of an item:
#   the name in its first column (e.g. "retrieval_method") where it heads only
#   one row on the page and is no other id there, and otherwise the id of the
#   nearest preceding heading and the name (e.g. "image-cube-time").
# - Allow the names in the first column to wrap after an underscore, by
#   inserting <wbr> there.
TABLE = %r{<table class="(?:[^"]*\s)?(?:attribute|variable|mandatory-attribute)-table(?:\s[^"]*)?">.*?</table>}m
HEADING = %r{<h[2-6] id="([^"]+)"}
NAME = %r{<tr>(\s*<td><code[^>]*>)([^<]*)(</code>)}

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html"

  html = doc.output
  ids = html.scan(/\sid="([^"]+)"/).flatten

  # The rows of all tables, with the heading they stand under.
  rows = []
  html.scan(Regexp.union(HEADING, TABLE)) do
    match = Regexp.last_match
    if match[1]
      rows << [:heading, match[1]]
    else
      match[0].scan(NAME) { rows << [:row, Regexp.last_match[2]] }
    end
  end
  counts = Hash.new(0)
  rows.each { |kind, name| counts[name] += 1 if kind == :row }
  heading = nil
  row_ids = rows.filter_map do |kind, value|
    if kind == :heading
      heading = value
      nil
    elsif counts[value] == 1 && !ids.include?(value)
      value
    else
      "#{heading}-#{value}"
    end
  end
  duplicates = row_ids.tally.select { |_, n| n > 1 }.keys + (row_ids & ids)
  unless duplicates.empty?
    raise "#{doc.relative_path}: table rows with the same id: #{duplicates.uniq.join(', ')}"
  end

  doc.output = html.gsub(TABLE) do |table|
    # Take the groups before the inner gsub, which resets $1, $2 and $3.
    table.gsub(NAME) do
      open, name, close = $1, $2, $3
      %(<tr id="#{row_ids.shift}">#{open}#{name.gsub('_', '_<wbr>')}#{close})
    end
  end
end
