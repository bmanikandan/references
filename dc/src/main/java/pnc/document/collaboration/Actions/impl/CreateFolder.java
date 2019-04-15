package pnc.document.collaboration.Actions.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;
import com.squareup.okhttp.MediaType;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import pnc.document.collaboration.Actions.Action;
import pnc.document.collaboration.beans.GraphApiResponse;
import pnc.document.collaboration.beans.MyProfileResponse;
import pnc.document.collaboration.service.GraphApiService;
import pnc.document.collaboration.utils.Constants;

import java.util.List;
import java.util.UUID;

@Component
public class CreateFolder implements Action<String, String> {
    @Autowired
    private GraphApiService service;

    private final ObjectMapper MAPPER = new ObjectMapper();

    private OkHttpClient client = new OkHttpClient();

    @Override
    public String execute(String input) {
        try {
            MediaType mediaType = MediaType.parse("application/json");
            RequestBody body = RequestBody.create(mediaType, "{\n  \"name\": \"" + input + "\",\n  \"folder\": {}\n}");

            Request request = new Request.Builder()
                    .url(Constants.USER_LIST)
                    .post(body)
                    .addHeader("SdkVersion", Constants.SDK_VERSION)
                    .addHeader("Authorization", service.getAccessToken())
                    .addHeader("cache-control", "no-cache")
                    .addHeader("Postman-Token", UUID.randomUUID().toString())
                    .build();

            Response response = client.newCall(request).execute();
            JSONObject json = new JSONObject(response.body().string().toString());
            return "Created";
        }
        catch (Exception e) {
            System.err.println(e.getLocalizedMessage());
        }

        return null;
    }
}
