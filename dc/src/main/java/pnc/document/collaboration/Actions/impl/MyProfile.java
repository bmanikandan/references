package pnc.document.collaboration.Actions.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.Response;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import pnc.document.collaboration.Actions.Action;
import pnc.document.collaboration.beans.MyProfileResponse;
import pnc.document.collaboration.service.GraphApiService;
import pnc.document.collaboration.utils.Constants;

import java.util.UUID;

@Component
public class MyProfile implements Action<String, MyProfileResponse> {

    @Autowired
    private GraphApiService service;

    private final ObjectMapper MAPPER = new ObjectMapper();

    private OkHttpClient client = new OkHttpClient();

    @Override
    public MyProfileResponse execute(String input) {
        try {
            Request request = new Request.Builder()
                    .url(Constants.MY_PROFILE)
                    .get()
                    .addHeader("SdkVersion", Constants.SDK_VERSION)
                    .addHeader("Authorization", service.getAccessToken())
                    .addHeader("cache-control", "no-cache")
                    .addHeader("Postman-Token", UUID.randomUUID().toString())
                    .build();

            Response response = client.newCall(request).execute();
            return MAPPER.readValue(response.body().string(), MyProfileResponse.class);
        }
        catch (Exception e) {
            System.err.println(e.getLocalizedMessage());
        }

        return null;
    }
}
