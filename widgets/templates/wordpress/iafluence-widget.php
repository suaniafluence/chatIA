<?php
/**
 * Plugin Name: IAfluence Chatbot
 * Plugin URI: https://iafluence.fr
 * Description: Intègre un chatbot IA personnalisé sur votre site WordPress
 * Version: 1.0.0
 * Author: IAfluence
 * Author URI: https://iafluence.fr
 * Text Domain: iafluence-chatbot
 * Domain Path: /languages
 * License: GPL-2.0+
 */

// Si ce fichier est appelé directement, on sort
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Classe principale du plugin IAfluence Chatbot
 */
class IAfluence_Chatbot {
    /**
     * ID unique du client
     * @var string
     */
    private $client_id;
    
    /**
     * Options de configuration du chatbot
     * @var array
     */
    private $options;
    
    /**
     * URL du serveur IAfluence
     * @var string
     */
    private $server_url;
    
    /**
     * Constructeur
     */
    public function __construct() {
        // Initialisation des variables
        $this->client_id = '{{CLIENT_ID}}'; // Sera remplacé dynamiquement lors de la génération
        $this->server_url = '{{SERVER_URL}}'; // Sera remplacé dynamiquement lors de la génération
        
        // Chargement des options depuis la base de données
        $this->options = get_option('iafluence_chatbot_options', array(
            'position' => 'bottom-right',
            'primary_color' => '#4f46e5',
            'secondary_color' => '#ffffff',
            'chatbot_name' => 'Assistant IA',
            'welcome_message' => 'Bonjour ! Comment puis-je vous aider aujourd\'hui ?',
            'logo_url' => '',
            'show_branding' => true,
            'auto_open' => false,
            'delay_auto_open' => 5000,
            'custom_css' => '',
        ));
        
        // Hooks d'initialisation
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('wp_footer', array($this, 'render_chatbot_container'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'register_settings'));
        
        // Ajout d'un hook pour les mises à jour du plugin
        add_action('plugins_loaded', array($this, 'check_for_updates'));
    }
    
    /**
     * Enregistre les scripts et styles nécessaires
     */
    public function enqueue_scripts() {
        // Enregistrement du script principal
        wp_enqueue_script(
            'iafluence-chatbot-widget',
            $this->server_url . '/widgets/js/chatbot-widget.min.js',
            array(),
            '1.0.0',
            true
        );
        
        // Enregistrement des styles
        wp_enqueue_style(
            'iafluence-chatbot-styles',
            $this->server_url . '/widgets/css/chatbot-widget.min.css',
            array(),
            '1.0.0'
        );
        
        // Passage des options au script
        wp_localize_script(
            'iafluence-chatbot-widget',
            'iafluenceChatbotOptions',
            array(
                'client_id' => $this->client_id,
                'server_url' => $this->server_url,
                'options' => $this->options,
                'wp_rest_nonce' => wp_create_nonce('wp_rest'),
                'ajax_url' => admin_url('admin-ajax.php'),
            )
        );
        
        // Ajout du CSS personnalisé si défini
        if (!empty($this->options['custom_css'])) {
            wp_add_inline_style('iafluence-chatbot-styles', $this->options['custom_css']);
        }
    }
    
    /**
     * Affiche le conteneur HTML du chatbot
     */
    public function render_chatbot_container() {
        ?>
        <div id="iafluence-chatbot-container" 
             data-position="<?php echo esc_attr($this->options['position']); ?>"
             data-primary-color="<?php echo esc_attr($this->options['primary_color']); ?>"
             data-secondary-color="<?php echo esc_attr($this->options['secondary_color']); ?>"
             data-chatbot-name="<?php echo esc_attr($this->options['chatbot_name']); ?>"
             data-welcome-message="<?php echo esc_attr($this->options['welcome_message']); ?>"
             data-logo-url="<?php echo esc_url($this->options['logo_url']); ?>"
             data-show-branding="<?php echo $this->options['show_branding'] ? 'true' : 'false'; ?>"
             data-auto-open="<?php echo $this->options['auto_open'] ? 'true' : 'false'; ?>"
             data-delay-auto-open="<?php echo intval($this->options['delay_auto_open']); ?>"
        ></div>
        <?php
    }
    
    /**
     * Ajoute le menu d'administration
     */
    public function add_admin_menu() {
        add_options_page(
            'IAfluence Chatbot',
            'IAfluence Chatbot',
            'manage_options',
            'iafluence-chatbot',
            array($this, 'render_admin_page')
        );
    }
    
    /**
     * Enregistre les paramètres du plugin
     */
    public function register_settings() {
        register_setting('iafluence_chatbot_options', 'iafluence_chatbot_options');
        
        // Section générale
        add_settings_section(
            'iafluence_chatbot_general',
            'Paramètres généraux',
            array($this, 'render_general_section'),
            'iafluence-chatbot'
        );
        
        // Champs de la section générale
        add_settings_field(
            'chatbot_name',
            'Nom du chatbot',
            array($this, 'render_chatbot_name_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_general'
        );
        
        add_settings_field(
            'welcome_message',
            'Message de bienvenue',
            array($this, 'render_welcome_message_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_general'
        );
        
        add_settings_field(
            'position',
            'Position du chatbot',
            array($this, 'render_position_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_general'
        );
        
        // Section apparence
        add_settings_section(
            'iafluence_chatbot_appearance',
            'Apparence',
            array($this, 'render_appearance_section'),
            'iafluence-chatbot'
        );
        
        // Champs de la section apparence
        add_settings_field(
            'primary_color',
            'Couleur principale',
            array($this, 'render_primary_color_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_appearance'
        );
        
        add_settings_field(
            'secondary_color',
            'Couleur secondaire',
            array($this, 'render_secondary_color_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_appearance'
        );
        
        add_settings_field(
            'logo_url',
            'URL du logo',
            array($this, 'render_logo_url_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_appearance'
        );
        
        add_settings_field(
            'show_branding',
            'Afficher le branding IAfluence',
            array($this, 'render_show_branding_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_appearance'
        );
        
        add_settings_field(
            'custom_css',
            'CSS personnalisé',
            array($this, 'render_custom_css_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_appearance'
        );
        
        // Section comportement
        add_settings_section(
            'iafluence_chatbot_behavior',
            'Comportement',
            array($this, 'render_behavior_section'),
            'iafluence-chatbot'
        );
        
        // Champs de la section comportement
        add_settings_field(
            'auto_open',
            'Ouverture automatique',
            array($this, 'render_auto_open_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_behavior'
        );
        
        add_settings_field(
            'delay_auto_open',
            'Délai avant ouverture automatique (ms)',
            array($this, 'render_delay_auto_open_field'),
            'iafluence-chatbot',
            'iafluence_chatbot_behavior'
        );
    }
    
    /**
     * Affiche la page d'administration
     */
    public function render_admin_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        
        // Sauvegarde des options
        if (isset($_POST['iafluence_chatbot_options'])) {
            update_option('iafluence_chatbot_options', $_POST['iafluence_chatbot_options']);
            $this->options = get_option('iafluence_chatbot_options');
            echo '<div class="notice notice-success is-dismissible"><p>Paramètres sauvegardés avec succès.</p></div>';
        }
        
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            <p>Configurez votre chatbot IAfluence. Pour toute assistance, contactez <a href="mailto:support@iafluence.fr">support@iafluence.fr</a>.</p>
            
            <form method="post" action="options.php">
                <?php
                settings_fields('iafluence_chatbot_options');
                do_settings_sections('iafluence-chatbot');
                submit_button('Enregistrer les paramètres');
                ?>
            </form>
            
            <hr>
            
            <h2>Informations de connexion</h2>
            <p>ID Client: <code><?php echo esc_html($this->client_id); ?></code></p>
            <p>Serveur: <code><?php echo esc_html($this->server_url); ?></code></p>
            
            <h2>Prévisualisation</h2>
            <p>Voici un aperçu de votre chatbot avec les paramètres actuels :</p>
            <div id="iafluence-chatbot-preview" style="width: 100%; height: 500px; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; position: relative;">
                <iframe src="<?php echo esc_url($this->server_url . '/preview?client_id=' . $this->client_id); ?>" style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
        </div>
        <?php
    }
    
    /**
     * Rendu de la section générale
     */
    public function render_general_section() {
        echo '<p>Configurez les paramètres généraux de votre chatbot.</p>';
    }
    
    /**
     * Rendu du champ nom du chatbot
     */
    public function render_chatbot_name_field() {
        $value = isset($this->options['chatbot_name']) ? $this->options['chatbot_name'] : '';
        echo '<input type="text" name="iafluence_chatbot_options[chatbot_name]" value="' . esc_attr($value) . '" class="regular-text">';
        echo '<p class="description">Le nom qui sera affiché dans l\'en-tête du chatbot.</p>';
    }
    
    /**
     * Rendu du champ message de bienvenue
     */
    public function render_welcome_message_field() {
        $value = isset($this->options['welcome_message']) ? $this->options['welcome_message'] : '';
        echo '<textarea name="iafluence_chatbot_options[welcome_message]" rows="3" class="large-text">' . esc_textarea($value) . '</textarea>';
        echo '<p class="description">Le message qui sera affiché lorsque l\'utilisateur ouvre le chatbot pour la première fois.</p>';
    }
    
    /**
     * Rendu du champ position
     */
    public function render_position_field() {
        $value = isset($this->options['position']) ? $this->options['position'] : 'bottom-right';
        $positions = array(
            'bottom-right' => 'En bas à droite',
            'bottom-left' => 'En bas à gauche',
            'top-right' => 'En haut à droite',
            'top-left' => 'En haut à gauche',
        );
        
        echo '<select name="iafluence_chatbot_options[position]">';
        foreach ($positions as $key => $label) {
            echo '<option value="' . esc_attr($key) . '" ' . selected($value, $key, false) . '>' . esc_html($label) . '</option>';
        }
        echo '</select>';
        echo '<p class="description">La position du bouton de chat sur votre site.</p>';
    }
    
    /**
     * Rendu de la section apparence
     */
    public function render_appearance_section() {
        echo '<p>Personnalisez l\'apparence de votre chatbot.</p>';
    }
    
    /**
     * Rendu du champ couleur principale
     */
    public function render_primary_color_field() {
        $value = isset($this->options['primary_color']) ? $this->options['primary_color'] : '#4f46e5';
        echo '<input type="color" name="iafluence_chatbot_options[primary_color]" value="' . esc_attr($value) . '">';
        echo '<p class="description">La couleur principale utilisée pour le bouton et l\'en-tête du chatbot.</p>';
    }
    
    /**
     * Rendu du champ couleur secondaire
     */
    public function render_secondary_color_field() {
        $value = isset($this->options['secondary_color']) ? $this->options['secondary_color'] : '#ffffff';
        echo '<input type="color" name="iafluence_chatbot_options[secondary_color]" value="' . esc_attr($value) . '">';
        echo '<p class="description">La couleur secondaire utilisée pour le texte et les icônes.</p>';
    }
    
    /**
     * Rendu du champ URL du logo
     */
    public function render_logo_url_field() {
        $value = isset($this->options['logo_url']) ? $this->options['logo_url'] : '';
        echo '<input type="text" name="iafluence_chatbot_options[logo_url]" value="' . esc_attr($value) . '" class="regular-text">';
        echo '<button type="button" class="button button-secondary" id="iafluence-upload-logo">Sélectionner une image</button>';
        echo '<p class="description">L\'URL de votre logo. Laissez vide pour utiliser l\'icône par défaut.</p>';
        
        // Script pour l'upload de média
        ?>
        <script>
            jQuery(document).ready(function($) {
                $('#iafluence-upload-logo').click(function(e) {
                    e.preventDefault();
                    
                    var custom_uploader = wp.media({
                        title: 'Sélectionner un logo',
                        button: {
                            text: 'Utiliser cette image'
                        },
                        multiple: false
                    });
                    
                    custom_uploader.on('select', function() {
                        var attachment = custom_uploader.state().get('selection').first().toJSON();
                        $('input[name="iafluence_chatbot_options[logo_url]"]').val(attachment.url);
                    });
                    
                    custom_uploader.open();
                });
            });
        </script>
        <?php
    }
    
    /**
     * Rendu du champ afficher le branding
     */
    public function render_show_branding_field() {
        $value = isset($this->options['show_branding']) ? $this->options['show_branding'] : true;
        echo '<input type="checkbox" name="iafluence_chatbot_options[show_branding]" ' . checked($value, true, false) . ' value="1">';
        echo '<p class="description">Afficher "Propulsé par IAfluence" dans le pied de page du chatbot.</p>';
    }
    
    /**
     * Rendu du champ CSS personnalisé
     */
    public function render_custom_css_field() {
        $value = isset($this->options['custom_css']) ? $this->options['custom_css'] : '';
        echo '<textarea name="iafluence_chatbot_options[custom_css]" rows="5" class="large-text code">' . esc_textarea($value) . '</textarea>';
        echo '<p class="description">CSS personnalisé pour modifier l\'apparence du chatbot.</p>';
    }
    
    /**
     * Rendu de la section comportement
     */
    public function render_behavior_section() {
        echo '<p>Configurez le comportement de votre chatbot.</p>';
    }
    
    /**
     * Rendu du champ ouverture automatique
     */
    public function render_auto_open_field() {
        $value = isset($this->options['auto_op
(Content truncated due to size limit. Use line ranges to read in chunks)