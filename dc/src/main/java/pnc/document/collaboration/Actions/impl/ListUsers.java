package pnc.document.collaboration.Actions.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.Response;
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
public class ListUsers implements Action<String, List<MyProfileResponse>> {
    @Autowired
    private GraphApiService service;

    private final ObjectMapper MAPPER = new ObjectMapper();

    private OkHttpClient client = new OkHttpClient();

    @Override
    public List<MyProfileResponse> execute(String input) {
        try {
            Request request = new Request.Builder()
                    .url(Constants.USER_LIST)
                    .get()
                    .addHeader("SdkVersion", Constants.SDK_VERSION)
                    .addHeader("Authorization", service.getAccessToken())
                    .addHeader("cache-control", "no-cache")
                    .addHeader("Postman-Token", UUID.randomUUID().toString())
                    .build();

            Response response = client.newCall(request).execute();
            GraphApiResponse<MyProfileResponse>  userList = MAPPER.readValue(response.body().string(), new TypeReference<GraphApiResponse<MyProfileResponse>>() {});
            return userList.getValue();
        }
        catch (Exception e) {
            System.err.println(e.getLocalizedMessage());
        }

        return null;
    }
}
