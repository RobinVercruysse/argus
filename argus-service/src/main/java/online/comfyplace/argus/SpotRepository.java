package online.comfyplace.argus;

import com.fasterxml.jackson.databind.ObjectMapper;
import online.comfyplace.argus.model.Spot;
import org.springframework.stereotype.Repository;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Repository
public class SpotRepository {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    private final List<Spot> spots = new ArrayList<>();

    public void receiveSpot(final byte[] value) {
        try {
            addSpot(MAPPER.readValue(value, Spot.class));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public synchronized void addSpot(final Spot spot) {
        spots.add(spot);
    }

    public synchronized List<Spot> getSpots() {
        return new ArrayList<>(spots);
    }
}
