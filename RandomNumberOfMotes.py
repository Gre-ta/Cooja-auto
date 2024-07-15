import random
import os

def generate_random_positions(num_motes):
    positions = []
    for _ in range(num_motes):
        x = round(random.uniform(0, 300), 2)
        y = round(random.uniform(0, 300), 2)
        positions.append((x, y))
    return positions

def generate_simulation_config(num_motes, c_file, transmit_range, sim_name):
    positions = generate_random_positions(num_motes)

    motes_config = ""
    motes_list = ""
    bounds = ""
    for i, (x, y) in enumerate(positions, start=1):
        motes_config += f"""
      <mote>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="{x}" y="{y}" />
        </interface_config>
        <interface_config>
          org.contikios.cooja.mspmote.interfaces.MspMoteID
          <id>{i}</id>
        </interface_config>
      </mote>"""
        motes_list += f"      <mote>{i}</mote>\n"
        bounds += f'    <bounds x="{x}" y="{y}" height="166" width="1280" z="2" />\n'

    simulation_config = f"""<?xml version="1.0" encoding="UTF-8"?>
<simconf version="2022112801">
  <simulation>
    <title>{sim_name}</title>
    <randomseed>{random.randint(100000, 999999)}</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>
      org.contikios.cooja.radiomediums.UDGM
      <transmitting_range>{transmit_range}</transmitting_range>
      <interference_range>{transmit_range * 2}</interference_range>
      <success_ratio_tx>1.0</success_ratio_tx>
      <success_ratio_rx>1.0</success_ratio_rx>
    </radiomedium>
    <events>
      <logoutput>40000</logoutput>
    </events>
    <motetype>
      org.contikios.cooja.mspmote.SkyMoteType
      <description>Sky Mote Type #1</description>
      <source>[CONTIKI_DIR]/examples/nullnet/{c_file}</source>
      <commands>make -j$(CPUS) {c_file.split('.')[0]}.sky TARGET=sky</commands>
      <firmware>[CONTIKI_DIR]/examples/nullnet/build/sky/{c_file.split('.')[0]}.sky</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyFlash</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyCoffeeFilesystem</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.Msp802154Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspSerial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyTemperature</moteinterface>
      {motes_config}
    </motetype>
  </simulation>
  <plugin>
    org.contikios.cooja.plugins.Visualizer
    <plugin_config>
      <moterelations>true</moterelations>
      <skin>org.contikios.cooja.plugins.skins.IDVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.GridVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.TrafficVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.UDGMVisualizerSkin</skin>
      <viewport>1.260669461391327 0.0 0.0 1.260669461391327 18.307830732154333 -4.506051924748429</viewport>
    </plugin_config>
{bounds}
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.LogListener
    <plugin_config>
      <filter />
      <formatted_time />
      <coloring />
    </plugin_config>
    <bounds x="400" y="160" height="240" width="880" z="3" />
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.TimeLine
    <plugin_config>
{motes_list}
      <showRadioRXTX />
      <showRadioHW />
      <showLEDs />
      <zoomfactor>500.0</zoomfactor>
    </plugin_config>
    <bounds x="0" y="395" height="166" width="1280" z="2" />
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Notes
    <plugin_config>
      <notes>Enter notes here</notes>
      <decorations>true</decorations>
    </plugin_config>
    <bounds x="400" y="0" height="160" width="880" z="1" />
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.ScriptRunner
    <plugin_config>
      <script>
TIMEOUT(2000000);
log.log("Starting logger");

var sendTime = 0;
var receiveTime = 0;

while (true) {{
  if (msg) {{
    // Check if the message is a sent message
    if (msg.contains("Sent")) {{
      sendTime = time;
    }}
    // Check if the message is a received message
    if (msg.contains("Received")) {{
      receiveTime = time;
      var elapsedTime = receiveTime - sendTime;
      log.log("Message Round Trip Time: " + elapsedTime + " ms\\n");
    }}
    
    log.log(time + " " + id + " " + msg + "\\n");
  }}

  YIELD();
}}  
      </script>
      <active>true</active>
    </plugin_config>
  </plugin>
</simconf>"""
    return simulation_config

def save_simulation_config(file_path, config_content):
    with open(file_path, 'w') as file:
        file.write(config_content)

# Parameters
c_files = [
    "nullnet-broadcast1s.c", "nullnet-broadcast10s.c", "nullnet-broadcast1m.c", 
    "nullnet-broadcast10m.c", "nullnet-broadcast10ms.c", "nullnet-broadcast100ms.c", 
    "nullnet-broadcast50.c", "nullnet-broadcast60.c", "nullnet-broadcast120.c" "nullnet-broadcast900.c"
]
file_dir = "/home/vagrant/contiki-ng/tools/cooja/CscFile"
num_configs = 10  # Number of different configurations to generate

for i in range(num_configs):
    num_motes = random.randint(10, 50)  # Random number of motes
    c_file = random.choice(c_files)  # Random .c file
    transmit_range = round(random.uniform(30.0, 100.0), 2)  # Random transmitting range
    sim_name = f"MySimulation_{i+1}"  # Unique simulation name
    file_name = f"simulation_{i+1}.csc"
    file_path = os.path.join(file_dir, file_name)

    config_content = generate_simulation_config(num_motes, c_file, transmit_range, sim_name)
    save_simulation_config(file_path, config_content)
    print(f"Simulation configuration saved to {file_path}")
