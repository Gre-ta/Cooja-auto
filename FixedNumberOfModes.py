import random

def generate_random_positions(num_motes):
    positions = []
    for _ in range(num_motes):
        x = round(random.uniform(0, 300), 2)
        y = round(random.uniform(0, 300), 2)
        positions.append((x, y))
    return positions

def generate_simulation_config(num_motes, c_file):
    positions = generate_random_positions(num_motes)

    motes_config = ""
    motes_list = ""
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

    # Bounds dynamically generated for motes
    bounds = ""
    for (x, y) in positions:
        bounds += f'    <bounds x="{x}" y="{y}" height="166" width="1280" z="2" />\n'

    # Bounds dynamically generated for Visualizer plugin
    visualizer_bounds = ""
    for (x, y) in positions:
        visualizer_bounds += f'    <bounds x="{x}" y="{y}" height="166" width="1280" z="2" />\n'

    simulation_config = f"""<?xml version="1.0" encoding="UTF-8"?>
<simconf version="2022112801">
  <simulation>
    <title>My simulation</title>
    <randomseed>123456</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>
      org.contikios.cooja.radiomediums.UDGM
      <transmitting_range>50.0</transmitting_range>
      <interference_range>100.0</interference_range>
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
      <commands>make -j$(CPUS) nullnet-broadcast1.sky TARGET=sky</commands>
      <firmware>[CONTIKI_DIR]/examples/nullnet/build/sky/nullnet-broadcast1.sky</firmware>
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
      <script><![CDATA[
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
      ]]></script>
      <active>true</active>
    </plugin_config>
  </plugin>
</simconf>"""
    return simulation_config

def save_simulation_config(file_path, config_content):
    with open(file_path, 'w') as file:
        file.write(config_content)

# Parameters
num_motes = 30  # You can change the number of motes
c_file = "nullnet-broadcast1.c"  # Change this as needed
file_path = "/home/vagrant/contiki-ng/tools/cooja/CscFile/simulation.csc"

# Generate and save the configuration
config_content = generate_simulation_config(num_motes, c_file)
save_simulation_config(file_path, config_content)
print(f"Simulation configuration saved to {file_path}")
