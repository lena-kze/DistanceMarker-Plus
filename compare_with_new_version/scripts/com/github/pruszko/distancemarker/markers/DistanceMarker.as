package com.github.pruszko.distancemarker.markers
{
   import com.github.pruszko.distancemarker.DistanceMarkerFlash;
   import com.github.pruszko.distancemarker.config.Config;
   import com.github.pruszko.distancemarker.utils.Disposable;
   import flash.display.Shape;
   import flash.display.Sprite;
   import flash.filters.BlurFilter;
   import flash.filters.GlowFilter;
   import flash.text.AntiAliasType;
   import flash.text.TextField;
   import flash.text.TextFieldAutoSize;
   import flash.text.TextFieldType;
   import flash.text.TextFormat;
   
   public class DistanceMarker extends Sprite implements Disposable
   {
      
      private var _app:DistanceMarkerFlash;
      
      private var _currentDistance:Number = -1;
      
      private var _textField:TextField = new TextField();
      
      private var _shape:Shape;
      
      public function DistanceMarker(param1:DistanceMarkerFlash)
      {
         super();
         this._app = param1;
         if(this.config.drawTextShadow)
         {
            this._shape = new Shape();
            this._shape.alpha = 0.35;
            this._shape.filters = [new BlurFilter(10,10,2)];
            this.addChild(this._shape);
         }
         this._textField.alpha = this.config.textAlpha;
         this._textField.antiAliasType = AntiAliasType.NORMAL;
         this._textField.autoSize = TextFieldAutoSize.CENTER;
         this._textField.background = false;
         this._textField.border = false;
         this._textField.multiline = false;
         this._textField.selectable = false;
         this._textField.type = TextFieldType.DYNAMIC;
         this._textField.wordWrap = false;
         this._textField.defaultTextFormat = new TextFormat("$TitleFont",this.config.textSize,this.config.textColor);
         if(this.config.drawTextOutline)
         {
            this._textField.filters = [new GlowFilter(0,1,2,2,2,2)];
         }
         var _loc2_:String = this.config.drawDistanceUnit ? " m" : "";
         this._textField.text = "?" + _loc2_;
         this._textField.x = -this._textField.textWidth / 2;
         this.addChild(this._textField);
         if(this.config.drawTextShadow)
         {
            this.updateBackgroundShape();
         }
      }
      
      public function set currentDistance(param1:Number) : void
      {
         this._currentDistance = param1;
         var _loc2_:String = this.config.drawDistanceUnit ? " m" : "";
         this._textField.text = param1.toFixed(this.config.decimalPrecision).toString() + _loc2_;
         this._textField.x = -this._textField.textWidth / 2;
         if(this.config.drawTextShadow)
         {
            this.updateBackgroundShape();
         }
      }
      
      private function updateBackgroundShape() : void
      {
         var _loc1_:Number = this._textField.x + 2;
         var _loc2_:Number = this._textField.y + 2;
         var _loc3_:Number = this._textField.textWidth;
         var _loc4_:Number = this._textField.textHeight;
         var _loc5_:Number = 10;
         var _loc6_:Number = 2;
         this._shape.graphics.clear();
         this._shape.graphics.beginFill(0);
         this._shape.graphics.drawEllipse(_loc1_ - _loc5_,_loc2_ - _loc6_,_loc3_ + 2 * _loc5_,_loc4_ + 2 * _loc6_);
         this._shape.graphics.endFill();
      }
      
      public function get currentDistance() : Number
      {
         return this._currentDistance;
      }
      
      public function disposeState() : void
      {
         this.removeChild(this._textField);
         this._textField = null;
         if(this.config.drawTextShadow)
         {
            this.removeChild(this._shape);
            this._shape = null;
         }
         this._app = null;
      }
      
      public function isInBounds(param1:Number, param2:Number) : Boolean
      {
         return this._textField.hitTestPoint(param1,param2);
      }
      
      private function get config() : Config
      {
         return this._app.config;
      }
   }
}

