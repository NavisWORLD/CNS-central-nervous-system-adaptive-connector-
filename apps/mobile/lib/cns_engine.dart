import 'dart:math' as math;

class SensoryInput {
  const SensoryInput({
    this.audioRms = 0.2,
    this.frequencyHz = 220,
    this.spectralFlatness = 0.25,
    this.phaseRad = 0,
    this.phaseVelocity = 0,
    this.avCoherence = 0.8,
    this.pleasure = 0,
    this.arousal = 0.4,
    this.dominance = 0.5,
    this.motionEnergy = 0.2,
    this.luminance = 0.5,
    this.entropy = 0.5,
  });

  final double audioRms;
  final double frequencyHz;
  final double spectralFlatness;
  final double phaseRad;
  final double phaseVelocity;
  final double avCoherence;
  final double pleasure;
  final double arousal;
  final double dominance;
  final double motionEnergy;
  final double luminance;
  final double entropy;
}

class CnsMobileResult {
  const CnsMobileResult({
    required this.response,
    required this.sensory12d,
    required this.context42d,
    required this.adaptive54d,
    required this.coherence,
    required this.iteration,
  });

  final String response;
  final List<double> sensory12d;
  final List<double> context42d;
  final List<double> adaptive54d;
  final double coherence;
  final int iteration;
}

class CnsMobileEngine {
  CnsMobileEngine({int seed = 707}) : _random = math.Random(seed);

  static const double phi = 1.618033988749895;
  final math.Random _random;
  List<double> _previous54 = List<double>.filled(54, 0);
  int _iteration = 0;

  int get iteration => _iteration;

  double _unit(double value, double min, double max) {
    if (!value.isFinite || max <= min) return 0.0;
    return ((value - min) / (max - min)).clamp(0.0, 1.0).toDouble();
  }

  double _signed(double value, double scale) {
    if (!value.isFinite || scale <= 0) return 0.0;
    return (value / scale).clamp(-1.0, 1.0).toDouble();
  }

  double _tanh(double value) {
    if (!value.isFinite) return value.isNegative ? -1.0 : 1.0;
    if (value >= 20.0) return 1.0;
    if (value <= -20.0) return -1.0;
    final e2x = math.exp(2.0 * value);
    return (e2x - 1.0) / (e2x + 1.0);
  }

  List<double> encode12(SensoryInput s) {
    final rms = _unit(s.audioRms, 0.0, 1.0);
    final freq = _unit(s.frequencyHz, 0.0, 4000.0);
    final flat = _unit(s.spectralFlatness, 0.0, 1.0);
    final phase = math.sin(s.phaseRad.isFinite ? s.phaseRad : 0.0);
    final phaseV = _signed(s.phaseVelocity, 10.0);
    final av = _unit(s.avCoherence, 0.0, 1.0) * 2.0 - 1.0;
    final p = s.pleasure.clamp(-1.0, 1.0).toDouble();
    final a = _unit(s.arousal, 0.0, 1.0) * 2.0 - 1.0;
    final d = _unit(s.dominance, 0.0, 1.0) * 2.0 - 1.0;
    final audioPsi = math.sin(2.0 * math.pi * freq) * rms;
    final phiH = math.cos(2.0 * math.pi * ((freq * phi) % 1.0)) * (0.25 + 0.75 * rms);
    final motion = _unit(s.motionEnergy, 0.0, 1.0);
    final luminance = _unit(s.luminance, 0.0, 1.0);
    final mlc = ((1.0 - math.min(1.0, (motion - luminance).abs())) * 2.0 - 1.0).toDouble();
    final ent = _unit(s.entropy, 0.0, 1.0) * 2.0 - 1.0;
    final frequencyMass = (math.sqrt(math.max(rms, 0.0)) * (2.0 * freq - 1.0)).toDouble();
    return <double>[
      frequencyMass,
      phase,
      2.0 * flat - 1.0,
      phaseV,
      av,
      p,
      a,
      d,
      audioPsi,
      phiH,
      mlc,
      ent,
    ];
  }

  List<double> expand42(List<double> x12, Map<String, double> context) {
    if (x12.length != 12) throw ArgumentError('12D state must contain 12 values');
    final coherence = (context['coherence'] ?? 0.0).clamp(-1.0, 1.0).toDouble();
    final entropy = (context['entropy'] ?? 0.5).clamp(0.0, 1.0).toDouble() * 2.0 - 1.0;
    final loop = _tanh((context['loop'] ?? _iteration.toDouble()) / 16.0);
    final mean = x12.reduce((a, b) => a + b) / 12.0;
    final energy = math.sqrt(x12.map((v) => v * v).reduce((a, b) => a + b) / 12.0);
    final spread = math.sqrt(x12.map((v) => math.pow(v - mean, 2).toDouble()).reduce((a, b) => a + b) / 12.0);

    final extra = <double>[];
    for (var i = 0; i < 30; i++) {
      final source = x12[i % 12];
      final partner = x12[(i * 5 + 3) % 12];
      final harmonic = math.sin(source * (i + 1) * 0.31 + partner * 0.17);
      final control = i % 5 == 0
          ? coherence
          : i % 5 == 1
              ? entropy
              : i % 5 == 2
                  ? loop
                  : i % 5 == 3
                      ? energy
                      : spread;
      extra.add(_tanh(0.62 * source + 0.23 * partner + 0.15 * control + 0.08 * harmonic));
    }
    return <double>[...x12, ...extra];
  }

  List<double> adapt54(List<double> x42, double entropy) {
    if (x42.length != 42) throw ArgumentError('42D state must contain 42 values');
    final next = List<double>.filled(54, 0.0);
    for (var i = 0; i < 42; i++) {
      final recurrence = _previous54[i];
      final partner = x42[(i * 7 + 1) % 42];
      next[i] = _tanh(0.72 * x42[i] + 0.18 * recurrence + 0.10 * partner);
    }
    final ent = entropy.clamp(0.0, 1.0).toDouble() * 2.0 - 1.0;
    for (var i = 0; i < 12; i++) {
      final base = x42[(i * 3) % 42];
      final prior = _previous54[42 + i];
      final memory = _previous54[i];
      final jitter = (_random.nextDouble() - 0.5) * 0.02;
      next[42 + i] = _tanh(0.50 * base + 0.28 * prior + 0.17 * memory + 0.05 * ent + jitter);
    }
    _previous54 = List<double>.from(next);
    _iteration += 1;
    return next;
  }

  CnsMobileResult run(String prompt, SensoryInput sensory) {
    final x12 = encode12(sensory);
    final x42 = expand42(x12, {
      'coherence': sensory.avCoherence,
      'entropy': sensory.entropy,
      'loop': _iteration.toDouble(),
    });
    final x54 = adapt54(x42, sensory.entropy);
    final meanAbs = x54.map((v) => v.abs()).reduce((a, b) => a + b) / 54.0;
    final coherence = (1.0 - (meanAbs - 0.45).abs()).clamp(0.0, 1.0).toDouble();
    final tone = coherence > 0.75
        ? 'stable'
        : coherence > 0.5
            ? 'adaptive'
            : 'exploratory';
    final response = 'CNS mobile cycle $_iteration complete. State is $tone with coherence '
        '${coherence.toStringAsFixed(3)}. Prompt: ${prompt.trim().isEmpty ? '(empty)' : prompt.trim()}';
    return CnsMobileResult(
      response: response,
      sensory12d: x12,
      context42d: x42,
      adaptive54d: x54,
      coherence: coherence,
      iteration: _iteration,
    );
  }
}
