package life.andre.sms487.activities;

import android.app.Activity;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.text.Editable;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.NonNull;

import androidx.core.app.NotificationCompat;
import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;

import java.util.List;

import life.andre.sms487.R;
import life.andre.sms487.events.MessagesStateChanged;
import life.andre.sms487.logging.Logger;
import life.andre.sms487.messages.MessageContainer;
import life.andre.sms487.messages.MessageStorage;
import life.andre.sms487.settings.AppSettings;
import life.andre.sms487.system.PermissionsChecker;
import life.andre.sms487.utils.BgTask;

public class MainActivity extends Activity {
    private final LogUpdater logUpdater = new LogUpdater(this::showLogsFromLogger);
    private final EventBus eventBus = EventBus.getDefault();
    private boolean lockSettingsSave = false;
    private EditText serverUrlInput;
    private TextView messagesField;
    private TextView logsField;

    private Button settingBtn;

    private Button testBtn;

    private Button btnClear;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        PermissionsChecker.check(this);

        findViewComponents();
        bindEvents();
    }

    @Override
    protected void onStart() {
        super.onStart();
        showSettings();
        showMessages();
        logUpdater.run();
        eventBus.register(this);
    }

    @Override
    protected void onStop() {
        logUpdater.disable();
        eventBus.unregister(this);
        super.onStop();
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onMessagesStateChanged(MessagesStateChanged event) {
        showMessages();
    }

    private void findViewComponents() {
        serverUrlInput = findViewById(R.id.serverUrlInput);
        messagesField = findViewById(R.id.messagesField);
        logsField = findViewById(R.id.logsField);
        settingBtn = findViewById(R.id.btnSetting);
        testBtn = findViewById(R.id.btnTest);
        btnClear = findViewById(R.id.btnClear);
    }

    private void bindEvents() {
        serverUrlInput.setOnEditorActionListener((v, actionId, event) -> {
            saveServerUrl();
            return false;
        });
        settingBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                Intent myIntent = new Intent(view.getContext(), MainSetting.class);
                startActivityForResult(myIntent, 0);
            }
        });

        testBtn.setOnClickListener(v->{
            CharSequence name = "channelTest";
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel("channelTest", name, importance);
            // Register the channel with the system; you can't change the importance
            // or other notification behaviors after this
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);

            NotificationCompat.Builder builder =
                    new NotificationCompat.Builder(this,"channelTest")
                            .setSmallIcon(R.drawable.ic_notification)
                            .setContentTitle("Notifications Example")
                            .setContentText("This is a test notification");

            Intent notificationIntent = new Intent(this, MainActivity.class);
            PendingIntent contentIntent = PendingIntent.getActivity(this, 0, notificationIntent,
                    PendingIntent.FLAG_UPDATE_CURRENT);
            builder.setContentIntent(contentIntent);

            // Add as notification
            NotificationManager manager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            manager.notify(0, builder.build());
        });

        btnClear.setOnClickListener(v->{logsField.setText("");Logger.clear();});
    }

    private void showSettings() {
        BgTask.run(this::getSettingsToShow).onSuccess(this::fillSettingFields);
    }

    @NonNull
    private SettingsToShow getSettingsToShow() {
        AppSettings st = AppSettings.getInstance();
        return new SettingsToShow(st.getServerUrl(), st.getServerKey());
    }

    private void fillSettingFields(@NonNull SettingsToShow st) {
        lockSettingsSave = true;
        showServerUrl(st.serverUrl);
        lockSettingsSave = false;
    }

    public void showServerUrl(@NonNull String serverUrl) {
        if (serverUrlInput != null) {
            serverUrlInput.setText(serverUrl);
        }
    }

    void saveServerUrl() {
        if (serverUrlInput == null || lockSettingsSave) {
            return;
        }

        BgTask.run(() -> {
            Editable serverUrlText = serverUrlInput.getText();
            if (serverUrlText != null) {
                AppSettings.getInstance().saveServerUrl(serverUrlText.toString());
            }
            return null;
        });
    }

    private void showMessages() {
        if (messagesField == null) {
            return;
        }
        BgTask.run(this::getMessages).onSuccess(this::setMessagesToField);
    }

    @NonNull
    private List<MessageContainer> getMessages() {
        return MessageStorage.getInstance().getMessagesTail();
    }

    private void setMessagesToField(@NonNull List<MessageContainer> messages) {
        StringBuilder msgVal = new StringBuilder();

        for (MessageContainer message : messages) {
            msgVal.append(message.getAddressFrom())
                    .append('\t').append(message.getDateTime())
                    .append("\nSent: ").append(message.isSent() ? "yes" : "no")
                    .append('\n')
                    .append(message.getBody()).append("\n\n");
        }

        messagesField.setText(msgVal.toString().trim());
    }

    private void showLogsFromLogger() {
        if (logsField == null) {
            return;
        }

        StringBuilder logs = new StringBuilder();
        for (String logLine : Logger.getMessages()) {
            logs.append(logLine).append('\n');
        }
        logsField.setText(logs.toString().trim());
    }

    private static class LogUpdater implements Runnable {
        public static final int DELAY = 1000;

        private final Handler handler = new Handler(Looper.getMainLooper());
        private final Runnable action;

        public LogUpdater(Runnable action) {
            this.action = action;
        }

        @Override
        public synchronized void run() {
            action.run();
            handler.postDelayed(this, DELAY);
        }

        public synchronized void disable() {
            handler.removeCallbacks(this);
        }
    }

    private static class SettingsToShow {
        @NonNull
        final String serverUrl;
        @NonNull
        final String serverKey;

        SettingsToShow(@NonNull String serverUrl, @NonNull String serverKey) {
            this.serverUrl = serverUrl;
            this.serverKey = serverKey;
        }
    }
}
