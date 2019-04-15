package pnc.document.collaboration.beans;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class GraphApiResponse<T> implements Serializable {
    public static final long serialVersionUID = 1L;

    private List<T> value = null;

    public List<T> getValue() {
        if (value == null) {
            value = new ArrayList<>();
        }
        return value;
    }
}
