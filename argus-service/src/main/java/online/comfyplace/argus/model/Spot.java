package online.comfyplace.argus.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDateTime;

public class Spot {
    private String transmitter;
    private String receiver;
    @JsonProperty(value = "sig")
    private String signal;
    private double time;
    @JsonProperty(value = "frame_type")
    private int frameType;
    @JsonProperty(value = "frame_subtype")
    private int frameSubtype;
    private int channel;
    @JsonProperty(value = "transmitter_name")
    private String transmitterName;

    public String getTransmitter() {
        return transmitter;
    }

    public String getReceiver() {
        return receiver;
    }

    public String getSignal() {
        return signal;
    }

    public double getTime() {
        return time;
    }

    public int getFrameType() {
        return frameType;
    }

    public int getFrameSubtype() {
        return frameSubtype;
    }

    public int getChannel() {
        return channel;
    }

    public String getTransmitterName() {
        return transmitterName;
    }
}
