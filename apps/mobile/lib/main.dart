import 'package:flutter/material.dart';
import 'cns_engine.dart';

void main() {
  runApp(const CnsBridgeApp());
}

class CnsBridgeApp extends StatelessWidget {
  const CnsBridgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'CNS Bridge',
      themeMode: ThemeMode.dark,
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        colorSchemeSeed: const Color(0xFF7C8CFF),
        scaffoldBackgroundColor: const Color(0xFF080D18),
        useMaterial3: true,
        cardTheme: const CardThemeData(
          color: Color(0xFF111827),
          elevation: 0,
          margin: EdgeInsets.zero,
        ),
        inputDecorationTheme: const InputDecorationTheme(
          filled: true,
          fillColor: Color(0xFF0D1424),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(14)),
            borderSide: BorderSide.none,
          ),
        ),
      ),
      home: const CnsHomePage(),
    );
  }
}

class CnsHomePage extends StatefulWidget {
  const CnsHomePage({super.key});

  @override
  State<CnsHomePage> createState() => _CnsHomePageState();
}

class _CnsHomePageState extends State<CnsHomePage> {
  final _engine = CnsMobileEngine();
  final _prompt = TextEditingController(text: 'Choose the next action.');

  double _audioRms = 0.20;
  double _frequency = 220;
  double _flatness = 0.25;
  double _phase = 0;
  double _phaseVelocity = 0;
  double _coherence = 0.80;
  double _pleasure = 0;
  double _arousal = 0.40;
  double _dominance = 0.50;
  double _motion = 0.20;
  double _luminance = 0.50;
  CnsMobileResult? _result;
  int _page = 0;

  @override
  void dispose() {
    _prompt.dispose();
    super.dispose();
  }

  SensoryInput get _sensory => SensoryInput(
        audioRms: _audioRms,
        frequencyHz: _frequency,
        spectralFlatness: _flatness,
        phaseRad: _phase,
        phaseVelocity: _phaseVelocity,
        avCoherence: _coherence,
        pleasure: _pleasure,
        arousal: _arousal,
        dominance: _dominance,
        motionEnergy: _motion,
        luminance: _luminance,
        entropy: 0.5,
      );

  void _runCycle() {
    FocusScope.of(context).unfocus();
    setState(() {
      _result = _engine.run(_prompt.text, _sensory);
      _page = 1;
    });
  }

  @override
  Widget build(BuildContext context) {
    final pages = <Widget>[
      _controlPage(),
      _statePage(),
      _aboutPage(),
    ];
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        titleSpacing: 20,
        title: const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('CNS BRIDGE', style: TextStyle(fontWeight: FontWeight.w800, letterSpacing: 1.4)),
            Text('Adaptive Connector Mobile', style: TextStyle(fontSize: 11, color: Color(0xFF9BA9C8))),
          ],
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: Chip(
              avatar: const Icon(Icons.memory_rounded, size: 16),
              label: Text('Loop ${_engine.iteration}'),
            ),
          ),
        ],
      ),
      body: SafeArea(child: pages[_page]),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _page,
        onDestinationSelected: (value) => setState(() => _page = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.tune_rounded), label: 'Control'),
          NavigationDestination(icon: Icon(Icons.hub_rounded), label: 'State'),
          NavigationDestination(icon: Icon(Icons.info_outline_rounded), label: 'About'),
        ],
      ),
    );
  }

  Widget _controlPage() {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
      children: [
        _heroCard(),
        const SizedBox(height: 14),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const _SectionTitle(icon: Icons.chat_bubble_outline_rounded, title: 'Prompt'),
                const SizedBox(height: 12),
                TextField(
                  controller: _prompt,
                  minLines: 3,
                  maxLines: 6,
                  decoration: const InputDecoration(hintText: 'What should the CNS process?'),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 14),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const _SectionTitle(icon: Icons.sensors_rounded, title: 'Sensory state'),
                const SizedBox(height: 8),
                _slider('Audio RMS', _audioRms, 0, 1, (v) => _audioRms = v),
                _slider('Frequency Hz', _frequency, 0, 4000, (v) => _frequency = v, decimals: 0),
                _slider('Spectral flatness', _flatness, 0, 1, (v) => _flatness = v),
                _slider('A/V coherence', _coherence, 0, 1, (v) => _coherence = v),
                _slider('Arousal', _arousal, 0, 1, (v) => _arousal = v),
                _slider('Dominance', _dominance, 0, 1, (v) => _dominance = v),
                _slider('Pleasure', _pleasure, -1, 1, (v) => _pleasure = v),
                _slider('Motion energy', _motion, 0, 1, (v) => _motion = v),
                _slider('Luminance', _luminance, 0, 1, (v) => _luminance = v),
                _slider('Geometric phase', _phase, -3.14159, 3.14159, (v) => _phase = v),
                _slider('Phase velocity', _phaseVelocity, -10, 10, (v) => _phaseVelocity = v),
              ],
            ),
          ),
        ),
        const SizedBox(height: 18),
        FilledButton.icon(
          onPressed: _runCycle,
          icon: const Icon(Icons.play_arrow_rounded),
          label: const Padding(
            padding: EdgeInsets.symmetric(vertical: 14),
            child: Text('RUN LOCAL CNS CYCLE', style: TextStyle(fontWeight: FontWeight.w800, letterSpacing: .7)),
          ),
        ),
      ],
    );
  }

  Widget _heroCard() {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        gradient: const LinearGradient(
          colors: [Color(0xFF1A2140), Color(0xFF10182A)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('LOCAL • PRIVATE • FAIL-SOFT', style: TextStyle(fontSize: 11, color: Color(0xFF9FB0FF), fontWeight: FontWeight.w800)),
          const SizedBox(height: 8),
          const Text('12D → 42D → 54D', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900)),
          const SizedBox(height: 8),
          Text(
            'Run the mobile reference state loop without sending the prompt or state vectors to a remote service.',
            style: TextStyle(color: Colors.white.withValues(alpha: .72), height: 1.35),
          ),
        ],
      ),
    );
  }

  Widget _slider(String label, double value, double min, double max, ValueChanged<double> setter, {int decimals = 2}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 5),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(child: Text(label, style: const TextStyle(color: Color(0xFFC6D1EA)))),
              Text(value.toStringAsFixed(decimals), style: const TextStyle(fontFeatures: [FontFeature.tabularFigures()])),
            ],
          ),
          Slider(
            value: value.clamp(min, max),
            min: min,
            max: max,
            onChanged: (v) => setState(() => setter(v)),
          ),
        ],
      ),
    );
  }

  Widget _statePage() {
    final result = _result;
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
      children: [
        if (result == null)
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  const Icon(Icons.hub_outlined, size: 48, color: Color(0xFF8EA0FF)),
                  const SizedBox(height: 12),
                  const Text('No cycle yet', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 6),
                  const Text('Run a local CNS cycle from the Control tab to populate state telemetry.', textAlign: TextAlign.center),
                  const SizedBox(height: 16),
                  OutlinedButton(onPressed: () => setState(() => _page = 0), child: const Text('Open controls')),
                ],
              ),
            ),
          )
        else ...[
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: [
              _metric('12D', result.sensory12d.length.toString(), Icons.sensors_rounded),
              _metric('42D', result.context42d.length.toString(), Icons.account_tree_rounded),
              _metric('54D', result.adaptive54d.length.toString(), Icons.hub_rounded),
              _metric('Coherence', result.coherence.toStringAsFixed(3), Icons.graphic_eq_rounded),
            ],
          ),
          const SizedBox(height: 14),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const _SectionTitle(icon: Icons.bolt_rounded, title: 'Cycle result'),
                  const SizedBox(height: 12),
                  Text(result.response, style: const TextStyle(fontSize: 16, height: 1.4)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),
          _vectorCard('12D sensory vector', result.sensory12d),
          const SizedBox(height: 14),
          _vectorCard('42D context vector', result.context42d),
          const SizedBox(height: 14),
          _vectorCard('54D adaptive vector', result.adaptive54d),
        ],
      ],
    );
  }

  Widget _metric(String label, String value, IconData icon) {
    return SizedBox(
      width: 160,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Row(
            children: [
              Icon(icon, color: const Color(0xFF91A2FF)),
              const SizedBox(width: 10),
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(label, style: const TextStyle(fontSize: 11, color: Color(0xFF9BA9C8))),
                Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
              ]),
            ],
          ),
        ),
      ),
    );
  }

  Widget _vectorCard(String title, List<double> values) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontWeight: FontWeight.w800)),
            const SizedBox(height: 12),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: [
                for (var i = 0; i < values.length; i++)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                    decoration: BoxDecoration(color: const Color(0xFF0D1424), borderRadius: BorderRadius.circular(9)),
                    child: Text('${i + 1}: ${values[i].toStringAsFixed(2)}', style: const TextStyle(fontSize: 11)),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _aboutPage() {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
      children: const [
        Card(
          child: Padding(
            padding: EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _SectionTitle(icon: Icons.info_outline_rounded, title: 'About this app'),
                SizedBox(height: 12),
                Text(
                  'CNS Bridge Mobile is the cross-platform companion for the public COSMOS/Davis CNS adaptive connector reference architecture. It demonstrates a local 12-channel sensory state, 42-channel context expansion, and 54-channel recurrent adaptive state.',
                  style: TextStyle(height: 1.45),
                ),
                SizedBox(height: 12),
                Text(
                  'The mobile implementation is an interoperable companion implementation, not a claim that these channels are extra physical spatial dimensions and not a substitute for validating hardware or scientific claims.',
                  style: TextStyle(color: Color(0xFF9BA9C8), height: 1.45),
                ),
              ],
            ),
          ),
        ),
        SizedBox(height: 14),
        Card(
          child: Padding(
            padding: EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _SectionTitle(icon: Icons.verified_outlined, title: 'Distribution'),
                SizedBox(height: 12),
                Text('Android builds produce a release APK. iOS builds produce simulator and unsigned device app bundles; App Store/TestFlight or direct device installation requires Apple signing credentials.'),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle({required this.icon, required this.title});
  final IconData icon;
  final String title;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 20, color: const Color(0xFF91A2FF)),
        const SizedBox(width: 8),
        Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
      ],
    );
  }
}
