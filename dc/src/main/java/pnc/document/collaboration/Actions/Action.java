package pnc.document.collaboration.Actions;

public interface Action<T, R> {
    public abstract R execute(T object);
}
