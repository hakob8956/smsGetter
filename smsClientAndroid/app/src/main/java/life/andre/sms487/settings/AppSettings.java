package life.andre.sms487.settings;

import android.content.Context;

import androidx.annotation.NonNull;

import java.util.Objects;
import java.util.UUID;

import life.andre.sms487.views.Toaster;

@SuppressWarnings("SameParameterValue")
public class AppSettings {

    public static final String SERVER_URL = "Server URL";
    public static final String SERVER_KEY = "Server key";
    public static final String HEALTH_URL = "Health URL";
    public static final String NEED_TYPE_NOTIFICATION = "Notification message type";
    public static final String NEED_TYPE_SMS = "SMS message type";
    public static final String FILTER_VALUE = "";

    // Default values
    public static final String SERVER_URL_VALUE = "SERVER_URL_VALUE";
    public static final String SERVER_AUTH_VALUE = "SERVER_AUTH_VALUE";
    public static final String SERVER_KEY_VALUE = UUID.randomUUID().toString();
    public static final String HEALTH_URL = "Health URL";
    public static final String HEALTH_URL_VALUE = "https://monitor.hakob.org/mobile";
    public static final String HEALTH_URL_VALUE = "HEALTH_URL/mobile";

    private static final int TYPE_STRING = 0;
    private static final int TYPE_BOOL = 1;

    private static AppSettings instance;

    @NonNull
    private final AppSettingStorage storage;

    public static void init(@NonNull Context ctx) {
        instance = new AppSettings(ctx);
        instance.saveSecretKey(false);
    }

    @NonNull
    public static AppSettings getInstance() {
        return Objects.requireNonNull(instance, "Not initialized");
    }

    private AppSettings(@NonNull Context ctx) {
        storage = new AppSettingStorage(ctx);
    }

    @NonNull
    public String getServerUrl() {
        return getString(SERVER_URL, SERVER_URL_VALUE);
    }

    @NonNull
    public String getAuthKey() {
        return SERVER_AUTH_VALUE;
    }

    @NonNull
    public String getServerKey() {
        return getString(SERVER_KEY, SERVER_KEY_VALUE);
    }

    @NonNull
    public String getHealthUrl() {
        return getString(HEALTH_URL, HEALTH_URL_VALUE);
    }

    public boolean getNeedNotificationType(){
        return getBool(NEED_TYPE_NOTIFICATION);
    }

    public boolean getNeedSMSType(){
        return getBool(NEED_TYPE_SMS);
    }
    public String getFilter(){
        return getString(FILTER_VALUE);
    }

    public void saveServerUrl(@NonNull String serverUrl) {
        saveValue(SERVER_URL, serverUrl);
    }

    public void saveHealthUrl(@NonNull String healthUrl) {
        saveValue(HEALTH_URL, healthUrl);
    }

    public void saveSecretKey(boolean deleteExistKey) {
        if(getServerKey().equals("") || deleteExistKey)
            saveValue(SERVER_KEY, UUID.randomUUID().toString());
    }

    public void saveFilter(@NonNull String filterValue) {
        saveValue(FILTER_VALUE, filterValue );
    }

    public void saveNeedNotificationType(boolean needNotification){
        saveValue(NEED_TYPE_NOTIFICATION, needNotification);
    }

    public void saveNeedSMSType(boolean needSMSType){
        saveValue(NEED_TYPE_SMS, needSMSType);
    }

    @NonNull
    private String getString(@NonNull String name) {
        String val = getSettingsItem(name).strVal;
        return val == null ? "" : val;
    }

    @NonNull
    private String getString(@NonNull String name, @NonNull String defaultValue) {
        String val = getSettingsItem(name).strVal;
        return val == null ? defaultValue : val;
    }

    private boolean getBool(@NonNull String name) {
        return getSettingsItem(name).boolVal;
    }

    private void saveValue(@NonNull String name, @NonNull String val) {
        String msg = saveSettingsItemToStorage(name, TYPE_STRING, val, false);
        Toaster.getInstance().show(msg);
    }

    private void saveValue(@NonNull String name, boolean val) {
        String msg = saveSettingsItemToStorage(name, TYPE_BOOL, "", val);
        Toaster.getInstance().show(msg);
    }

    @NonNull
    private AppSettingStorage.SettingsItem getSettingsItem(@NonNull String name) {
        return storage.get(name);
    }

    @NonNull
    private String saveSettingsItemToStorage(@NonNull String name, int type, @NonNull String strVal, boolean boolVal) {
        switch (type) {
            case TYPE_STRING:
                return saveStringToStorage(name, strVal);
            case TYPE_BOOL:
                return saveBoolToStorage(name, boolVal);
        }

        return "Error: unknown setting";
    }

    @NonNull
    private String saveStringToStorage(@NonNull String name, @NonNull String val) {
        storage.set(name, val.trim());
        return name + " saved";
    }

    @NonNull
    private String saveBoolToStorage(@NonNull String name, boolean val) {
        storage.set(name, val);
        return name + " is now " + val;
    }
}
