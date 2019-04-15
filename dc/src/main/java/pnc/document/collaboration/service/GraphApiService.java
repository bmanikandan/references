package pnc.document.collaboration.service;

import com.squareup.okhttp.MediaType;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pnc.document.collaboration.config.AppConfigration;

import java.net.URLEncoder;

@Service
public class GraphApiService {
    @Autowired
    private AppConfigration config;

    public String getAccessToken() throws Exception {
        OkHttpClient client = new OkHttpClient();
        MediaType mediaType = MediaType.parse("application/x-www-form-urlencoded");
        // Secret Key is hardcoded to avoid Encode issue and prevent from account lock
        RequestBody body = RequestBody.create(mediaType, "grant_type=password&client_id=" + config.getClientId()
                + "&client_secret=%23%2B%3B%2Bo%7C_.%26%2F!%5D(-c*%3D%3F%2B%7Dy*%3D%3A%3D(%40%5E%3B%40-E%7D%25%40A1*%7B)%7Ci7%5D%26%7Bv%3Bd%7B)%3E"
                + "&scope=" + URLEncoder.encode(config.getScopes(), "UTF-8")
                + "&userName=" + URLEncoder.encode(config.getUserName(), "UTF-8")
                + "&password=" + URLEncoder.encode(config.getUserPassword(), "UTF-8")
                + "&undefined=");
        Request request = new Request.Builder()
                .url("https://login.microsoftonline.com/" + config.getTenantId() + "/oauth2/v2.0/token")
                .post(body)
                .addHeader("Content-Type", "application/x-www-form-urlencoded")
                .addHeader("SdkVersion", "postman-graph/v1.0")
                .addHeader("cache-control", "no-cache")
                .addHeader("Postman-Token", "af1e6470-514e-43c4-8f87-8c1296269e00")
                .build();
        com.squareup.okhttp.Response response = client.newCall(request).execute();
        JSONObject json = new JSONObject(response.body().string().toString());
        return json.getString("access_token");
    }
}
