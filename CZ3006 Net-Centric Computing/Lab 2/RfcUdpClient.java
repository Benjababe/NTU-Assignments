import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class RfcUdpClient {
	static int QOTD_PORT = 17;
	static String SERVER_NAME = "swlab2-c.scse.ntu.edu.sg";
	// static String SERVER_NAME = "localhost";

	public static void main(String[] args) {
		// 1. Open UDP socket
		DatagramSocket socket = null;

		try {
			InetAddress serverAddr = InetAddress.getByName(SERVER_NAME);
			socket = new DatagramSocket();
			socket.connect(serverAddr, QOTD_PORT);
			System.out.println("Client connected to " + serverAddr.getCanonicalHostName() + ":17");
		}

		catch (SocketException | UnknownHostException e) {
			e.printStackTrace();
		}

		try {
			// 1.5 Prepare message to be sent
			String message = "Benjamin, SSP1, 172.21.147.125";
			byte[] buffer = message.getBytes("UTF-8");

			// 2. Send UDP request to server
			DatagramPacket request = new DatagramPacket(buffer, buffer.length);
			System.out.println("Sending message...");
			socket.send(request);
			System.out.println("Message sent!");

			// 3. Receive UDP reply from server
			byte[] replyBuffer = new byte[512];
			DatagramPacket reply = new DatagramPacket(replyBuffer, replyBuffer.length);
			System.out.println("Waiting for reply...");
			socket.receive(reply);

			// 4. Process the reply from server
			String replyStr = new String(replyBuffer);
			System.out.println("Received reply: " + replyStr);
		}

		catch (IOException e) {
			e.printStackTrace();
		}
	}

}
