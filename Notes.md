```
import io.netty.handler.logging.LogLevel;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.jetty.client.api.Request;
import org.eclipse.jetty.http.HttpHeader;
import org.eclipse.jetty.util.ssl.SslContextFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Description;
import org.springframework.http.client.reactive.JettyClientHttpConnector;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.transport.logging.AdvancedByteBufFormat;

import java.net.URI;

import static com.att.idp.logger.LoggingEnhancer.enhance;
import static com.att.idp.logger.RequestLogger.logRequest;
import static com.att.idp.logger.ResponseLogger.logResponse;

@Slf4j
//@ConfigurationProperties(prefix = "reactive-api-client")
@Configuration
public class WebClientConfig {

    // jetty HttpClient
    @Bean
    public HttpClient jettyHttpClient() {
        SslContextFactory.Client sslContextFactory = new SslContextFactory.Client();
        HttpClient httpClient = new HttpClient(sslContextFactory){
            @Override
            public Request newRequest(URI uri) {
                Request request = super.newRequest(uri);
                return enhance(request);
            }
        };
        return httpClient;
    }

    @Bean
    @Description("idp webclient builder")
    public WebClient webClient(WebClient.Builder builder, ReactorClientHttpConnector reactorClientHttpConnector) {
        return builder
//                .clientConnector(new JettyClientHttpConnector(jettyHttpClient()))
                .clientConnector(reactorClientHttpConnector)
                .build();
    }

    // reactive http client to use wireTap
    @Bean
    public ReactorClientHttpConnector wiretappedConnector(boolean isDebug) {
        reactor.netty.http.client.HttpClient httpClient =
                reactor.netty.http.client.HttpClient.create()
                        .wiretap(
                                this.getClass().getCanonicalName(), LogLevel.INFO, AdvancedByteBufFormat.TEXTUAL);
        return new ReactorClientHttpConnector(httpClient);
    }
}
```
