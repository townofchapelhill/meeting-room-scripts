# meeting_room_scripts
A list of meeting room scripts for the Chapel Hill Open Data portal. Data is retrieved through an XML feed at http://kb.demcosoftware.com/article.php?id=720.

<strong>New Versions:</strong>

The updated scripts for the meeting room data now retrieve both future meeting room reservations and past meeting room reervations.  The script "updated_meetings.py" retrieves reservation data for up to 30 days into the future, the range can be extended as desired.

<strong>IMPORTANT NOTE</strong>

This version of "aggregate_reservations.py" is different from the version that's running on the server.  This version is set to retrieve as many historical records as the API will allow you to retrieve in one go.  The script on the server just appends the previous day's reservations to the master CSV.

In the event that the master CSV is lost, you can use this version of "aggregate_reservations.py" to recreate it.

<pre>
 _____ _                      _   _   _ _ _ _ 
/  __ \ |                    | | | | | (_) | |
| /  \/ |__   __ _ _ __   ___| | | |_| |_| | |
| |   | '_ \ / _` | '_ \ / _ \ | |  _  | | | |
| \__/\ | | | (_| | |_) |  __/ | | | | | | | |
 \____/_| |_|\__,_| .__/ \___|_| \_| |_/_|_|_|
                  | |                         
                  |_|       
</pre>           
