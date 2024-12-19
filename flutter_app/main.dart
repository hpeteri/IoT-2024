import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  MyAppState createState() => MyAppState();
}

class MyAppState extends State<MyApp> {
  bool? serverResponse;
  bool monitoring = false;
  bool loading = false;
  Timer? monitoringTimer;
  bool? serverResponse2;
  
  // fetch data from server
  Future<void> fetchReady() async {
    final url2 = Uri.parse('http://130.231.14.3:5000/ready');
    try {
      final response2 = await http.get(url2);

      if (response2.statusCode == 200) {
        final data2 = jsonDecode(response2.body);
        setState(() {
          serverResponse2 = data2['value'];
        });
      }
      else {
        print('Failed to fetch data: ${response2.statusCode}');
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  // fetch data from the server
  Future<void> fetchBrew({bool showloading = true}) async {
    if (showloading) {
      setState(() {
        loading = true;
      });
    }

    final url = Uri.parse('http://130.231.14.3:5000/brewing');
    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          serverResponse = data['value'];
        });
      } else {
        print('Failed to fetch data: ${response.statusCode}');
      }
    } catch (e) {
      print('Error: $e');
    } finally {
      if (showloading) {
        setState(() {
          loading = false;
        });
      }
    }
  }


  // start monitoring
  void startMonitoring() async {
    if (monitoring) return;

    setState(() {
      monitoring = true;
    });

    await fetchBrew();

    await fetchReady();
    // update the states
    monitoringTimer = Timer.periodic(Duration(seconds: 3), (timer) async {
      await fetchBrew(showloading: false);
      await fetchReady();
    });
  }
  // monitor stop
  void stopMonitoring() {
    setState(() {
      monitoring = false;
      monitoringTimer?.cancel();
      monitoringTimer = null;
    });
  }
  // cleanup
  @override
  void dispose() {
    monitoringTimer?.cancel();
    super.dispose();
  }
  // interface build
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: Text('Kiltis Coffee Scanner'),
          centerTitle: true,
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // show loading spinner
              if (loading)
                CircularProgressIndicator()
              // show first screen
              else if (serverResponse == null)
                Text(
                  'Want to know the coffee situation?',
                  style: TextStyle(fontSize: 20),
                  textAlign: TextAlign.center,
                )
              // show ready
              else if (serverResponse2 == true)
              Column(
                children: [
                  Image.asset('assets/covfeepotfull.png', height: 300, width: 300),
                  SizedBox(height:10),
                  Text('Coffee is ready!', style: TextStyle(fontSize: 20), 
                    textAlign: TextAlign.center,)
              ],)
              // show empty and brewing
              else
                Column(
                  children: [
                    serverResponse!
                        ? Image.asset('assets/covfeepotreal2.gif', height: 300, width: 300)
                        : Image.asset('assets/covfeepotempty.png', height: 300, width: 300),
                    SizedBox(height: 10),
                    Text(
                      serverResponse!
                          ? 'Coffee is brewing!'
                          : 'No coffee :(',
                      style: TextStyle(fontSize: 20),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),

              SizedBox(height: 20),

              ElevatedButton(
                onPressed: loading
                    ? null 
                    : (monitoring ? stopMonitoring : startMonitoring),
                child: Text(
                  monitoring
                      ? 'Stop scanning'
                      : (serverResponse == null
                          ? 'Start scanning for coffee'
                          : 'Start scanning for updates'),
                ),
              ),

              if (monitoring)
                Padding(
                  padding: const EdgeInsets.only(top: 10),
                  child: Text(
                    'Monitoring for coffee updates...',
                    style: TextStyle(fontSize: 16, color: Colors.grey),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
