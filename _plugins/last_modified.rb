# Set page.last_modified_date to the date of the last commit that changed the
# page's source file, for the "Page last modified" line of the theme's footer.
# Without git (or for uncommitted files) the date is left unset and the line is
# omitted. CI checks out the full history so that the dates are real.
require "open3"
require "time"

Jekyll::Hooks.register [:pages, :documents], :pre_render do |doc, payload|
  next if doc.data.key?("last_modified_date")

  path = doc.respond_to?(:path) ? doc.path : nil
  next unless path && File.file?(path)

  date, status = Open3.capture2("git", "log", "-1", "--format=%cI", "--", path, chdir: doc.site.source)
  next unless status.success? && !date.strip.empty?

  # The payload already holds a copy of the page data, so set the date there.
  payload["page"]["last_modified_date"] = Time.parse(date.strip)
end
