package life.andre.sms487.network;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import life.andre.sms487.settings.AppSettings;

public class NetworkUtils {

    private static HttpURLConnection createConnection(String urlStr, String key, String authKey) throws IOException {
        URL url = new URL(urlStr);
        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
        urlConnection.setRequestMethod("POST");
        urlConnection.setRequestProperty("Cookie", "__Secure-Secret-Key=" + key + "; __Secure-Auth-Token=" + authKey);
        urlConnection.setDoOutput(true);
        return urlConnection;
    }

    public static void callHealthEndpoint() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    AppSettings appSettings = AppSettings.getInstance();
                    String healthUrl = appSettings.getHealthUrl();
                    String key = appSettings.getServerKey();
                    String authKey = appSettings.getAuthKey();

                    HttpURLConnection urlConnection = createConnection(healthUrl, key, authKey);

                    // Send POST request
                    OutputStream os = urlConnection.getOutputStream();
                    os.write(new byte[0]);
                    os.flush();
                    os.close();

                    int responseCode = urlConnection.getResponseCode();
                    if (responseCode == HttpURLConnection.HTTP_OK) {
                        BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                        String inputLine;
                        StringBuilder response = new StringBuilder();

                        while ((inputLine = in.readLine()) != null) {
                            response.append(inputLine);
                        }
                        in.close();

                        // Print the response or handle it as needed
                        System.out.println(response.toString());
                    } else {
                        System.out.println("POST request failed: " + responseCode);
                    }
                } catch (Exception e) {
                    // Print stack trace to standard error stream
                    e.printStackTrace(System.err);
                }
            }
        }).start();
    }

}
