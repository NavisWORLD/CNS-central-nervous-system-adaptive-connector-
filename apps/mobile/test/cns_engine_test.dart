import 'package:cns_bridge_mobile/cns_engine.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('mobile CNS preserves 12D 42D 54D contract and recurrence', () {
    final engine = CnsMobileEngine(seed: 707);
    const sensory = SensoryInput(
      audioRms: 0.2,
      frequencyHz: 220,
      arousal: 0.4,
      avCoherence: 0.8,
    );

    final first = engine.run('first cycle', sensory);
    final second = engine.run('second cycle', sensory);

    expect(first.sensory12d.length, 12);
    expect(first.context42d.length, 42);
    expect(first.adaptive54d.length, 54);
    expect(first.response, isNotEmpty);
    expect(first.iteration, 1);
    expect(second.iteration, 2);
    expect(second.adaptive54d, isNot(equals(first.adaptive54d)));
    expect(second.coherence, inInclusiveRange(0.0, 1.0));
  });
}
