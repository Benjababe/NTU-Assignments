import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

public class RfcUdpServer {
	static int QOTD_PORT = 17;
	static String QUOTE = "cao ni ma";

	public static void main(String[] args) {
		// 1. Open UDP socket at well-known port
		DatagramSocket socket = null;

		try {
			socket = new DatagramSocket(QOTD_PORT);
		}

		catch (SocketException e) {
			e.printStackTrace();
		}

		while (true) {
			try {
				// 2. Listen for UDP request from client
				byte[] buffer = new byte[512];
				DatagramPacket request = new DatagramPacket(buffer, buffer.length);
				System.out.println("Waiting for request...");
				socket.receive(request);

				// 2.5 Process client message
				String received = new String(buffer);
				System.out.println("Received text: " + received);

				// We need the client's IP and port to send the reply
				InetAddress clientAddr = request.getAddress();
				int clientPort = request.getPort();
				System.out.println("From client " + clientAddr.getCanonicalHostName());

				// 3. Send UDP reply to client
				String replyStr = QUOTE;
				byte[] replyBuffer = replyStr.getBytes("UTF-8");

				DatagramPacket reply = new DatagramPacket(replyBuffer, replyBuffer.length, clientAddr, clientPort);
				socket.send(reply);
				System.out.println("Quote sent");
			}

			catch (IOException e) {
				e.printStackTrace();
				socket.close();
				System.exit(-1);
			}
		}
	}

}
