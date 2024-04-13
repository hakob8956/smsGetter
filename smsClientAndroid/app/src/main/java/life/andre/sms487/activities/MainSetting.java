package life.andre.sms487.activities;
import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;
import androidx.annotation.NonNull;
import life.andre.sms487.R;
import life.andre.sms487.system.PermissionsChecker;
import life.andre.sms487.settings.AppSettings;
import life.andre.sms487.utils.BgTask;
import org.w3c.dom.Text;

public class MainSetting extends Activity {
    private Button btnBack;
    private CheckBox chkNotificationType;
    private CheckBox chkSMSType;
    private TextView txtSecretKey;
    private Button btnGenerateSecretKey;
    private Button btnCopySecretKey;
    private EditText txtFilter;
    private boolean lockSettingsSave = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.setting_main);
        PermissionsChecker.check(this);
        findViewComponents();
        defaultSettings();
        bindEvents();
    }

    @Override
    protected void onStart() {
        super.onStart();
        showSettings();
    }

    @Override
    protected void onStop() {
        super.onStop();
    }



    private void fillSettingFields(@NonNull MainSetting.SettingsToShow st) {
        lockSettingsSave = true;
        showNotificationType(st.notificationType);
        showSMSType(st.SMSType);
        showSecretKey(st.secretKey);
        showFilter(st.filter);
        lockSettingsSave = false;
    }
    private void findViewComponents() {
        btnBack = findViewById(R.id.btnMainScreen);
        chkNotificationType = findViewById(R.id.chkNotificationType);
        chkSMSType = findViewById(R.id.chkSMSType);
        txtSecretKey = findViewById(R.id.txtServerKey);
        btnGenerateSecretKey = findViewById(R.id.btnGenerate);
        btnCopySecretKey = findViewById(R.id.btnCopy);
        txtFilter = findViewById(R.id.txtFilter);
    }
    private void defaultSettings(){
        if (txtSecretKey != null)
            txtSecretKey.setEnabled(false);
    }
    private void bindEvents() {
        btnBack.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                Intent intent = new Intent();
                setResult(RESULT_OK, intent);
                finish();
            }
        });
        txtFilter.setOnEditorActionListener((v, actionId, event) -> {
            saveFilter();
            return false;
        });
        chkSMSType.setOnCheckedChangeListener((v, c) -> saveNeedSMSType());
        chkNotificationType.setOnCheckedChangeListener((v, c) -> saveNeedNotificationType());
        btnCopySecretKey.setOnClickListener(v->copySecretKey());
        btnGenerateSecretKey.setOnClickListener(v -> {saveSecretKey();});
    }

    private void copySecretKey(){
        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        ClipData clip = ClipData.newPlainText("secret Key",txtSecretKey.getText());
        clipboard.setPrimaryClip(clip);
    }

    private void showSettings() {
        BgTask.run(this::getSettingsToShow).onSuccess(this::fillSettingFields);
    }

    @NonNull
    private MainSetting.SettingsToShow getSettingsToShow() {
        AppSettings st = AppSettings.getInstance();
        return new MainSetting.SettingsToShow(st.getNeedNotificationType(),st.getNeedSMSType(),st.getServerKey(), st.getFilter());
    }
    void saveNeedSMSType() {
        if (chkSMSType == null || lockSettingsSave) {
            return;
        }

        BgTask.run(() -> {
            AppSettings.getInstance().saveNeedSMSType(chkSMSType.isChecked());
            return null;
        });
    }

    void saveNeedNotificationType() {
        if (chkNotificationType == null || lockSettingsSave) {
            return;
        }

        BgTask.run(() -> {
            AppSettings.getInstance().saveNeedNotificationType(chkNotificationType.isChecked());
            return null;
        });
    }

    void saveSecretKey() {
        if (lockSettingsSave)
            return;
        AppSettings.getInstance().saveSecretKey(true);
        showSettings();
    }
    void saveFilter() {
        if (txtFilter == null || lockSettingsSave) {
            return;
        }
        BgTask.run(() -> {
            Editable filterText = txtFilter.getText();
            if (filterText != null) {
                AppSettings.getInstance().saveFilter(filterText.toString());
            }
            return null;
        });
    }
    public void showNotificationType(boolean notificationType) {
        if (chkNotificationType != null) {
            chkNotificationType.setChecked(notificationType);
        }
    }
    public void showSMSType(boolean SMSType) {
        if (chkSMSType != null) {
            chkSMSType.setChecked(SMSType);
        }
    }

    public void showSecretKey(String secretKey) {
        if (txtSecretKey != null) {
            txtSecretKey.setText(secretKey);
        }
    }

    public void showFilter(String filterValue) {
        if (txtFilter != null) {
            txtFilter.setText(filterValue);
        }
    }

    private static class SettingsToShow {
        final boolean notificationType;
        final boolean SMSType;
        final String secretKey;
        final String filter;

        SettingsToShow(boolean notificationType, boolean SMSType, @NonNull String secretKey, @NonNull String filter) {
            this.SMSType = SMSType;
            this.notificationType = notificationType;
            this.secretKey = secretKey;
            this.filter = filter;
        }
    }
}

