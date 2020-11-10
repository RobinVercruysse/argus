package online.comfyplace.argus;

import online.comfyplace.argus.model.Spot;
import online.comfyplace.argus.model.TransmissionDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

@org.springframework.stereotype.Controller
public class Controller {
    @Autowired
    private SpotRepository spotRepository;

    @RequestMapping(method = RequestMethod.GET, path = "/transmissions", produces = "application/json")
    public ResponseEntity<Collection<TransmissionDTO>> getTransmissions() {
        final Map<String, TransmissionDTO> transmissions = new HashMap<>();
        for (final Spot spot : spotRepository.getSpots()) {
            if (transmissions.containsKey(spot.getTransmitter())) {
                transmissions.get(spot.getTransmitter()).out();
            } else if (transmissions.containsKey(spot.getReceiver())) {
                transmissions.get(spot.getReceiver()).in();
            } else {
                TransmissionDTO transmission = new TransmissionDTO(spot.getTransmitter(), spot.getReceiver());
                transmission.out();
                transmissions.put(spot.getTransmitter(), transmission);
            }
        }
        return ResponseEntity.ok(transmissions.values());
    }
}
