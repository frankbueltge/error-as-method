# Session 67 probe runner — CRuby. Same two modes, same conventions as
# probe_python.py: every answer a string, nothing normalised across runtimes.
require 'json'

SEEDS = JSON.parse(File.read(File.join(__dir__, 'seeds.json')))

def bits(x) = [x].pack('G').unpack1('H*')
def unbits(h) = [h].pack('H*').unpack1('G')
def cps(s) = s.codepoints.map { |c| format('U+%04X', c) }.join(' ')

# strict, whole-string conversion -- the nearest analogue of float()/Number()
def numify(s)
  bits(Float(s))
rescue ArgumentError, TypeError
  'error'
end

# The scalar set for L2/L3 -- this runtime's analogue of the classic set.
SCALARS = [['0', 0], ["''", ''], ["'0'", '0'], ['false', false],
           ['none', nil], ["'abc'", 'abc'], ['[]', []]].freeze

def emit
  a = {}
  # ---- Family S: answers that descend from the Unicode Character Database ----
  a['S1']  = cps('ß'.upcase)
  a['S2']  = cps('ﬁ'.upcase)
  a['S3']  = cps('İ'.downcase)
  a['S4']  = cps('ı'.upcase)
  a['S5']  = cps('ΟΔΟΣ'.downcase)
  a['S6']  = cps('ᏸ'.upcase)
  a['S7']  = cps('ჯ'.upcase)
  a['S8']  = cps("\u{10428}".upcase)
  a['S9']  = cps('ǳ'.upcase)
  a['S10'] = cps('ẞ'.downcase)

  # ---- Family I: answers written by hand, per runtime ----
  a['I1']  = (-7 % 3).to_s
  a['I2']  = (7 % -3).to_s
  a['I3']  = (-7 / 3).to_s
  a['I4']  = (0.1 + 0.2).to_s
  a['I5']  = (1.0 / 3).to_s
  a['I6']  = 1e21.to_s
  a['I7']  = (-0.0).to_s
  a['I8']  = [0.5, 1.5, 2.5, -0.5].map { |v| v.round.to_s }.join(' ')
  a['I9']  = ('10' < '9').to_s
  a['I10'] = ('' == 0).to_s
  a['I11'] = "\u{1d11e}".length.to_s
  a['I12'] = (0.1 + 0.2 == 0.3).to_s
  a['I13'] = [10, 9, 1].sort.join(' ')
  a['I14'] = (2**3**2).to_s
  a['I15'] = ['0x10', '010', '1e2', ' 12 '].map { |s| numify(s) }.join(' ')

  renderings = SEEDS.to_h { |s| [s['name'], unbits(s['bits']).to_s] }

  { 'runtime' => 'ruby', 'version' => RUBY_VERSION,
    'unicode_version' => 'not exposed by this runtime', 'answers' => a,
    'checks' => { 'L1_roundtrip' => l1, 'L2_loose_equality' => l2,
                  'L3_relational_coherence' => l3, 'L4_division_identity' => l4 },
    'renderings' => renderings }
end

# L1 -- does this runtime parse back its own default rendering of a double?
def l1
  detail = []
  SEEDS.each do |s|
    x = unbits(s['bits'])
    rendered = x.to_s
    back = begin
      bits(Float(rendered))
    rescue StandardError
      nil
    end
    detail << { 'seed' => s['name'], 'rendered' => rendered, 'back' => back } if back != s['bits']
  end
  { 'tested' => SEEDS.length, 'violations' => detail.length, 'detail' => detail }
end

# L2 -- is this runtime's own equality operator transitive over that set?
def l2
  viol = []
  SCALARS.each do |na, x|
    SCALARS.each do |nb, y|
      SCALARS.each do |nc, z|
        viol << [na, nb, nc] if (x == y) && (y == z) && !(x == z)
      end
    end
  end
  { 'operator' => '==', 'set_size' => SCALARS.length,
    'transitivity_violations' => viol.length, 'examples' => viol.first(5) }
end

# L3 -- if a<=b and a>=b, does this runtime also say a==b?
def l3
  viol = []
  incomparable = 0
  SCALARS.each do |na, x|
    SCALARS.each do |nb, y|
      begin
        le = (x <= y)
        ge = (x >= y)
      rescue StandardError
        incomparable += 1
        next
      end
      viol << [na, nb] if le && ge && !(x == y)
    end
  end
  { 'pairs' => SCALARS.length**2, 'incomparable' => incomparable,
    'violations' => viol.length, 'examples' => viol.first(5) }
end

# L4 -- does q*b + r == a hold, with this runtime's own division and % ?
def l4
  viol = []
  [-13, -8, -7, -1, 0, 1, 7, 8, 13].each do |a|
    [3, -3, 5, -5].each do |b|
      q = a / b
      r = a % b
      viol << [a, b, q, r] if q * b + r != a
    end
  end
  { 'pairs' => 36, 'violations' => viol.length, 'examples' => viol.first(5) }
end

def parse_mode
  JSON.parse($stdin.read).map do |s|
    begin
      bits(Float(s))
    rescue StandardError
      nil
    end
  end
end

puts JSON.generate((ARGV[0] || 'emit') == 'emit' ? emit : parse_mode)
