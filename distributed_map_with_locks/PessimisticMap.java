import com.hazelcast.client.HazelcastClient;
import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.map.IMap;

public class PessimisticMap {
    private static String MapName = "pessimistic-map";
    public static void run() {
        String key = "lab1-pessimistic-counter";

        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        IMap<String, Integer> map = hz.getMap(MapName);
        map.put(key, 0);
        hz.shutdown();

        for (int t=0; t<10; t++) {
          new Thread("" + t) {
            public void run() {
                HazelcastInstance hz = HazelcastClient.newHazelcastClient();
                IMap<String, Integer> map = hz.getMap(MapName);
                System.out.println( "Starting" );
                for (int k = 0; k < 10000; k++) {
                    map.lock( key );
                    try {
                        Integer counter = map.get( key );
                        map.put( key, ++counter );
                    } finally {
                        map.unlock( key );
                    }
                }
                System.out.println( "Finished! Result = " + map.get( key ) );
                hz.shutdown();
            }
          }.start();
        }
    }

    public static void destroy() {
        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        hz.getMap(MapName).destroy();
        hz.shutdown();
    }
}