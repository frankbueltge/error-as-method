# Ruby probe. Reads a job on stdin, answers on stdout, in its own words.
#
# Rendering:
#   default -- Time#to_s, documented as returning the time as a string in the form
#              "2007-11-19 08:37:48 -0600". Note that Ruby's DEFAULT already carries an offset;
#              of the five runtimes here it is the only one whose default does.
#   iso     -- Time#iso8601 from the stdlib 'time' library.
# Parsing:
#   Time.parse from the stdlib 'time' library. Its own documentation warns that it "uses
#   heuristics" and that unparseable components are taken from the current time.
# Numbers:
#   String#to_f (Ruby's lenient conversion: junk becomes 0.0) and Kernel#Float (strict, raises).

require 'json'
require 'time'

job = JSON.parse($stdin.read)
out = { 'runtime' => 'ruby', 'version' => RUBY_VERSION }

if job['instants']
  out['render'] = job['instants'].map do |e|
    r = { 'default' => nil, 'default_error' => nil, 'iso' => nil, 'iso_error' => nil }
    begin
      t = Time.at(e)
      r['default'] = t.to_s
    rescue StandardError => ex
      r['default_error'] = "#{ex.class}: #{ex.message}"
    end
    begin
      r['iso'] = Time.at(e).iso8601
    rescue StandardError => ex
      r['iso_error'] = "#{ex.class}: #{ex.message}"
    end
    r
  end
end

if job['strings']
  out['parse'] = job['strings'].map do |s|
    begin
      t = Time.parse(s)
      { 'status' => 'ok', 'epoch' => t.to_f }
    rescue StandardError => ex
      { 'status' => 'refused', 'error' => "#{ex.class}: #{ex.message}" }
    end
  end
end

if job['numbers']
  # JSON cannot carry NaN or Infinity; report them by name so nothing is silently coerced.
  enc = lambda { |x| x.is_a?(Float) && !x.finite? ? x.to_s : x }
  out['numparse'] = job['numbers'].map do |s|
    r = { 'lenient' => enc.call(s.to_f), 'strict' => nil }
    begin
      r['strict'] = enc.call(Float(s))
    rescue StandardError => ex
      r['strict'] = nil
      r['strict_error'] = ex.class.to_s
    end
    r
  end
end

$stdout.write(JSON.generate(out))
