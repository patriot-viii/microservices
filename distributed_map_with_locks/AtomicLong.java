import com.hazelcast.client.HazelcastClient;
import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.cp.IAtomicLong;

public class AtomicLong {
    private static String Key = "lab1-atomiclong-counter";

    public static void run() {
        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        IAtomicLong counter = hz.getCPSubsystem().getAtomicLong( Key );
        counter.set(0);
        hz.shutdown();

        for (int t=0; t<10; t++) {
          new Thread("" + t) {
            public void run() {
                HazelcastInstance hz = HazelcastClient.newHazelcastClient();
                IAtomicLong counter = hz.getCPSubsystem().getAtomicLong( Key );
                System.out.println( "Starting" );
                for (int k = 0; k < 10000; k++) {
                    counter.incrementAndGet();
                }
                System.out.printf( "Count is %s\n", counter.get() );
                hz.shutdown();
            }
          }.start();
        }
    }

    public static void destroy() {
        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        IAtomicLong counter = hz.getCPSubsystem().getAtomicLong( Key );        
        counter.destroy();
        hz.shutdown();
    }
}