package life.andre.sms487.network;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

public class HealthCheckWorker extends Worker {

    public HealthCheckWorker(@NonNull Context context, @NonNull WorkerParameters workerParams) {
        super(context, workerParams);
    }

    @NonNull
    @Override
    public Result doWork() {
        // Call the health endpoint
        NetworkUtils.callHealthEndpoint();
        // Indicate whether the work finished successfully with the Result
        return Result.success();
    }
}
