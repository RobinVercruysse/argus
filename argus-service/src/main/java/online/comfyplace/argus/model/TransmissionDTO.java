package online.comfyplace.argus.model;

public class TransmissionDTO {
    private final String mac1;
    private final String mac2;
    private int nrIn;
    private int nrOut;

    public TransmissionDTO(String mac1, String mac2) {
        this.mac1 = mac1;
        this.mac2 = mac2;
    }

    public String getMac1() {
        return mac1;
    }

    public String getMac2() {
        return mac2;
    }

    public int getNrIn() {
        return nrIn;
    }

    public int getNrOut() {
        return nrOut;
    }

    public void in() {
        nrIn++;
    }

    public void out() {
        nrOut++;
    }
}
